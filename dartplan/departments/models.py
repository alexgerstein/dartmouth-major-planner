from dartplan.database import db

class Department(db.Model):
    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), index = True, unique = True)
    abbr = db.Column(db.String(10), index = True, unique = True)

    courses = db.relationship('Course', backref = 'department')

    def __init__(self, name, abbr):
        self.name = name
        self.abbr = abbr

    def __repr__(self):
        return '%s' % (self.abbr)
