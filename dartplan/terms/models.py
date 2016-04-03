from dartplan.database import db


class Term(db.Model):
    __tablename__ = 'term'

    SEASONS = ["W", "S", "X", "F"]

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.SmallInteger)
    season = db.Column(db.String(15))

    offerings = db.relationship('Offering', backref='term', lazy='dynamic')

    def in_range(self, start_term, end_term):

        # Check if year is out of range
        if (self.year > end_term.year) or (self.year < start_term.year):
            return False

        # If year is same as start, check if season too soon
        elif (self.year == start_term.year):
            if (self.SEASONS.index(self.season) < self.SEASONS.index(start_term.season)):
                return False

        # If year is same as end, check if season too late
        elif (self.year == end_term.year):
            if (self.SEASONS.index(self.season) > self.SEASONS.index(end_term.season)):
                return False

        return True

    def __repr__(self):
        return '%s%s' % (str(self.year)[2:], self.season)
