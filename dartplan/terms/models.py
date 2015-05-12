from dartplan.database import db

SEASONS = ["W", "S", "X", "F"]


class Term(db.Model):
    __tablename__ = 'term'

    id = db.Column(db.Integer, primary_key = True)
    year = db.Column(db.SmallInteger)
    season = db.Column(db.String(15))

    offerings = db.relationship('Offering', backref = 'term', lazy='dynamic')

    def in_range(self, start_term, end_term):

        # Check if year is out of range
        if (self.year > end_term.year) or (self.year < start_term.year):
            return False

        # Check if year is definitively in the range
        elif (self.year < end_term.year) and (self.year > start_term.year):
            return True

        # Check if term is on boundary
        elif (self.season == start_term.season) and (self.year == start_term.year):
            return True
        elif (self.season == end_term.season) and (self.year == end_term.year):
            return True

        # If year is same as start, check if term fits
        elif (self.year == start_term.year):
            if (SEASONS.index(self.season) > SEASONS.index(start_term.season)):
                return True

        elif (self.year == end_term.year):
            if (SEASONS.index(self.season) < SEASONS.index(end_term.season)):
                return True

        return False

    def __repr__(self):
        return '%s%s' % (str(self.year)[2:], self.season)
