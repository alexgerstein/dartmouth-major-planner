from dartplan.database import db
from dartplan.models import Term

user_course = db.Table('user_course',
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('user.id')),
                       db.Column('offering_id', db.Integer,
                                 db.ForeignKey('offering.id')))

user_terms = db.Table("user_terms",
                      db.Column('user_id', db.Integer,
                                db.ForeignKey("user.id")),
                      db.Column("term_id", db.Integer,
                                db.ForeignKey("term.id")))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String(15), index=True, unique=True)
    full_name = db.Column(db.String(200))
    nickname = db.Column(db.String(64))
    grad_year = db.Column(db.SmallInteger)

    email_course_updates = db.Column(db.Boolean)
    email_Dartplan_updates = db.Column(db.Boolean)

    terms = db.relationship('Term',
                            secondary=user_terms, lazy='dynamic')

    courses = db.relationship('Offering',
                              secondary=user_course, backref='users',
                              lazy='dynamic')

    plans = db.relationship('Plan', lazy='dynamic',
                            cascade='all, delete-orphan')

    def __init__(self, full_name, netid):
        self.full_name = full_name
        self.netid = netid
        self.nickname = full_name
        self.email_Dartplan_updates = True
        self.email_course_updates = True

    def enroll(self, offering):
        if offering not in self.courses:
            self.courses.append(offering)
            db.session.commit()
        return self

    def drop(self, offering):
        deleted = False
        if offering in self.courses:
            self.courses.remove(offering)

            # Delete user-added offerings from db
            # if no users take the course anymore
            if offering.user_added == "Y":
                if not User.query.filter(User.courses.contains(offering)) \
                                 .first():
                    db.session.delete(offering)
                    deleted = True

            db.session.commit()
        return deleted

    def swap_onterm(self, term):
        if term in self.terms:

            # Remove all courses during new off-term
            for course in self.courses:
                if course.term is term:
                    self.drop(course)

            self.terms.remove(term)
        else:
            self.terms.append(term)
        db.session.commit()
        return self

    def get_all_terms(self):
        all_terms = []

        # Add Freshman Fall
        t = Term.query.filter_by(year=self.grad_year - 4,
                                 season=Term.SEASONS[3]).first()
        if t is None:
            t = Term(year=self.grad_year - 4, season=Term.SEASONS[3])
            db.session.add(t)

        all_terms.append(t)

        for year_diff in reversed(range(4)):
            for season in Term.SEASONS:
                t = Term.query.filter_by(year=self.grad_year - year_diff,
                                         season=season).first()
                if t is None:
                    t = Term(year=self.grad_year - year_diff, season=season)
                    db.session.add(t)

                all_terms.append(t)

        # Remove extra fall
        all_terms.remove(t)

        return all_terms

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return str(self.netid)
