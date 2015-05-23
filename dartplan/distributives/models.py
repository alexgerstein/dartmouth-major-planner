from dartplan.database import db

class Distributive(db.Model):
    __tablename__ = 'distributive'

    id = db.Column(db.Integer, primary_key = True)
    abbr = db.Column(db.String(10), index = True, unique = True)

    def __repr__(self):
        return '%s' % (self.abbr)

