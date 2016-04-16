from dartplan.database import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String(15), index=True, unique=True)
    full_name = db.Column(db.String(200))
    nickname = db.Column(db.String(64))
    grad_year = db.Column(db.SmallInteger)

    email_course_updates = db.Column(db.Boolean)
    email_Dartplan_updates = db.Column(db.Boolean)

    plans = db.relationship('Plan', lazy='dynamic',
                            cascade='all, delete-orphan')

    def __init__(self, full_name, netid, grad_year=None):
        self.full_name = full_name
        self.netid = netid
        self.nickname = full_name
        self.email_Dartplan_updates = True
        self.email_course_updates = True

        if grad_year:
            self.grad_year = grad_year

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return str(self.netid)
