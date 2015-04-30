from dartplan.database import db
from dartplan.models import Offering


user_course = db.Table('user_course',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('offering_id', db.Integer, db.ForeignKey('offering.id'))
)

user_terms = db.Table("user_terms",
    db.Column('user_id', db.Integer, db.ForeignKey("user.id")),
    db.Column("term_id", db.Integer, db.ForeignKey("term.id"))
)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    netid = db.Column(db.String(15), index = True, unique=True)
    full_name = db.Column(db.String(200))
    nickname = db.Column(db.String(64))
    grad_year = db.Column(db.SmallInteger)

    email_course_updates = db.Column(db.Boolean)
    email_Dartplan_updates = db.Column(db.Boolean)

    terms = db.relationship("Term",
        secondary=user_terms,
        lazy='dynamic')

    courses = db.relationship('Offering',
        secondary=user_course,
        backref ='users',
        lazy = 'dynamic')

    def __init__(self, full_name, netid):
        self.full_name = full_name
        self.netid = netid
        self.nickname = full_name
        self.email_Dartplan_updates = True
        self.email_course_updates = True

    def take(self, offering):
        if not self.is_taking(offering):
            self.courses.append(offering)
            db.session.commit()
            return self
        return None

    def drop(self, offering):
        if self.is_taking(offering):

            self.courses.remove(offering)
            db.session.commit()

            # Delete user-added offerings from db
            # if no users take the course anymore
            if offering.user_added == "Y":
                if User.query.filter(User.courses.contains(offering)).count() == 0:
                    db.session.delete(offering)
                    db.session.commit()

            return self

        return None

    def switch_hour(self, offering, hour):
        term = offering.get_term()
        course = offering.get_course()

        self.drop(offering)

        o1 = Offering.query.filter_by(course = course, term = term, hour = hour).first()
        if o1 is not None:
            self.take(o1)
            return o1.id

        return False


    def is_enrolled(self, term):
        return term in self.terms

    def add_term(self, term):
        if not self.is_enrolled(term):
            self.terms.append(term)
            db.session.commit()
            return self

    def remove_term(self, term):
        if self.is_enrolled(term):
            self.terms.remove(term)
            db.session.commit()
            return self

    def swap_onterm(self, term):
        if self.is_enrolled(term):

            # Remove all courses during new off-term
            for course in self.courses:
                if course.term is term:
                    self.drop(course)

            self.terms.remove(term)
        else:
            self.add_term(term)
        return self


    def is_taking(self, offering):
        taking = offering in self.courses.all()
        return taking

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return str(self.netid)
