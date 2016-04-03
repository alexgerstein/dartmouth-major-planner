from dartplan.database import db

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

    terms = db.relationship("Term",
                            secondary=plan_terms, lazy='dynamic')

    offerings = db.relationship('Offering',
                                secondary=plan_offerings, backref='plans',
                                lazy='dynamic')

    def drop(self, offering):
        if offering in self.offerings:
            self.offerings.remove(offering)
            db.session.commit()
        return self

    def enroll(self, offering):
        if offering not in self.offerings:
            self.offerings.append(offering)
            db.session.commit()
        return self

    def swap_onterm(self, term):
        if term in self.terms:
            # Remove all courses during new off-term
            for offering in self.offerings:
                if offering.term is term:
                    self.drop(offering)

            self.terms.remove(term)
        else:
            self.terms.append(term)
        db.session.commit()
        return self

    def __repr__(self):
        return 'Plan %d (User %d): %s' % (self.id, self.user_id, self.title)
