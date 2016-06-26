from dartplan.database import db


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Float)
    name = db.Column(db.String(300), index=True)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'),
                              index=True)

    offerings = db.relationship('Offering', backref='course')
    avg_median = db.Column(db.String(5))

    def __repr__(self):
        # Fix number repr if there are no sections (i.e. CS 1.0 should be CS 1)
        returned_number = self.number
        split_number = str(self.number).split(".")
        if split_number[1] == "0":
            returned_number = split_number[0]

        return '%s %s - %s' % (self.department.abbr, returned_number, self.name.encode('ascii', 'ignore'))
