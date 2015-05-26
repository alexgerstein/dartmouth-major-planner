from dartplan.database import db


offering_distribs = db.Table("offering_distribs",
                             db.Column('offering_id', db.Integer,
                                       db.ForeignKey("offering.id")),
                             db.Column("distributive_id", db.Integer,
                                       db.ForeignKey("distributive.id"))
                             )


class Offering(db.Model):
    __tablename__ = 'offering'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    term_id = db.Column(db.Integer, db.ForeignKey('term.id'))
    hour_id = db.Column(db.Integer, db.ForeignKey('hour.id'))
    desc = db.Column(db.Unicode(25000))

    median = db.Column(db.String(5))

    distributives = db.relationship("Distributive",
                                    secondary=offering_distribs,
                                    backref='offerings',
                                    lazy='dynamic')

    added = db.Column(db.String(2))
    user_added = db.Column(db.String(2))

    def __repr__(self):
        course_str = str(self.course)
        return course_str.split(" -")[0]

    def get_possible_hours(self):
        possible_hours = []
        for offering in Offering.query.filter_by(course_id=self.course_id,
                                                 term_id=self.term_id).all():
            possible_hours.append(offering.hour)
        return possible_hours
