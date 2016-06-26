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
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), index=True)
    term_id = db.Column(db.Integer, db.ForeignKey('term.id'), index=True)
    hour_id = db.Column(db.Integer, db.ForeignKey('hour.id'), index=True)
    desc = db.Column(db.Unicode(25000))

    median = db.Column(db.String(5), index=True)

    distributives = db.relationship("Distributive",
                                    secondary=offering_distribs,
                                    backref='offerings',
                                    lazy='dynamic')

    added = db.Column(db.String(2))
    user_added = db.Column(db.String(2))

    def __repr__(self):
        course_str = str(self.course)
        return course_str.split(" -")[0]
