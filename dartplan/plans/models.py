from dartplan.database import db
from dartplan.models import Term

plan_offerings = db.Table('plan_offerings',
                          db.Column('plan_id', db.Integer,
                                    db.ForeignKey('plan.id')),
                          db.Column('offering_id', db.Integer,
                                    db.ForeignKey('offering.id')))

plan_terms = db.Table('plan_terms',
                      db.Column('plan_id', db.Integer,
                                db.ForeignKey('plan.id')),
                      db.Column('term_id', db.Integer,
                                db.ForeignKey('term.id')))


class Plan(db.Model):
    __tablename__ = 'plan'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), default='Default')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User')
    terms = db.relationship("Term",
                            secondary=plan_terms, lazy='dynamic')

    offerings = db.relationship('Offering',
                                secondary=plan_offerings, backref='plans',
                                lazy='dynamic')

    def drop(self, offering):
        deleted = False
        if offering in self.offerings:
            self.offerings.remove(offering)
            db.session.commit()

        # Delete user-added offerings from db
        # if no users take the course anymore
        if not Plan.query.filter(Plan.offerings.contains(offering)).first():
            if offering.user_added == 'Y':
                db.session.delete(offering)
                deleted = True
        return deleted

    def enroll(self, offering):
        if offering not in self.offerings.all():
            self.offerings.append(offering)
            db.session.commit()
        return self

    def swap_onterm(self, term):
        if term in self.terms:
            # Remove all courses during new off-term
            for offering in self.offerings.filter_by(term=term):
                self.drop(offering)

            self.terms.remove(term)
        else:
            self.terms.append(term)
        db.session.commit()
        return self

    def reset_terms(self):
        terms = self._get_all_terms()

        # Clear all terms, start clean
        for term in self.terms:
            self.terms.remove(term)

        for term in terms:
            self.terms.append(term)

        db.session.commit()
        return self

    def _get_all_terms(self):
        all_terms = []

        # Add Freshman Fall
        t = Term.query.filter_by(year=self.user.grad_year - 4,
                                 season=Term.SEASONS[3]).first()
        if t is None:
            t = Term(year=self.user.grad_year - 4, season=Term.SEASONS[3])
            db.session.add(t)

        all_terms.append(t)

        for year_diff in reversed(range(4)):
            for season in Term.SEASONS:
                t = Term.query.filter_by(year=self.user.grad_year - year_diff,
                                         season=season).first()
                if t is None:
                    t = Term(year=self.user.grad_year - year_diff,
                             season=season)
                    db.session.add(t)

                all_terms.append(t)

        # Remove extra fall
        all_terms.remove(t)

        return all_terms

    def __repr__(self):
        return 'Plan %s (User %s)' % (self.title, self.user, )