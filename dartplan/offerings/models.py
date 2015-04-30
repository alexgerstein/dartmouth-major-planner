from dartplan.database import db
from dartplan.models import Hour, Term, Course


offering_distribs = db.Table("offering_distribs",
  db.Column('offering_id', db.Integer, db.ForeignKey("offering.id")),
  db.Column("distributive_id", db.Integer, db.ForeignKey("distributive.id"))
)

class Offering(db.Model):
  __tablename__ = 'offering'

  id = db.Column(db.Integer, primary_key = True)
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

  def __init__(self, course, term, hour, desc, user_added):
    self.course_id = course
    self.term_id = term
    self.hour_id = hour
    self.desc = desc
    self.user_added = user_added

  def get_full_name(self):
    return str(Course.query.get(self.course_id))

  def get_term(self):
    return Term.query.get(self.term_id)

  def get_hour(self):
    return Hour.query.get(self.hour_id)

  def get_course(self):
    return Course.query.get(self.course_id)

  def get_possible_hours(self):
    return [offering.get_hour()
            for offering in Offering.query.filter_by(course_id=self.course_id,
                                                     term_id=self.term_id)
                                          .all()]

  def change_period(self, hour):
    self.hour_id = hour.id
    db.session.commit()
    return self

  def add_distrib(self, distrib):
    if distrib not in self.distributives:
      self.distributives.append(distrib)
      db.session.commit()
      return self

  def change_desc(self, course_desc):
    self.desc = ""
    self.desc = course_desc
    db.session.commit()
    return self

  def mark(self, string):
    self.added = string
    return self

  def mark_empty(self):
    self.added = ""
    return self

  def mark_user_added(self):
    self.user_added = "Y"
    return self

  def __repr__(self):
    course_str = str(self.get_course())
    return course_str.split(" -")[0]
