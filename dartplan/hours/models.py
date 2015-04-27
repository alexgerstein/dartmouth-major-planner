from dartplan.database import db


class Hour(db.Model):
    __tablename__ = "hour"

    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(150), index=True, unique=True)
    offerings = db.relationship('Offering', backref='hour')

    def __init__(self, period):
        self.period = period

    def __repr__(self):
        if (self.period == "Arrange"):
            return 'Arr'

        return '%s' % (self.period)
