from dartplan.database import db
from dartplan.models import User, Hour, Term, Course


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
    return str(Course.query.filter_by(id = self.course_id).first())

  def get_term(self):
    return Term.query.filter_by(id = self.term_id).first()

  def get_hour(self):
    return Hour.query.filter_by(id = self.hour_id).first()

  def get_course(self):
    return Course.query.filter_by(id = self.course_id).first()

  def get_possible_hours(self):
    possible_hours = ""
    for offering in Offering.query.filter_by(course_id = self.course_id, term_id = self.term_id).all():
      possible_hours += str(offering.get_hour()) + "; "
    return possible_hours[:-2]

  def get_user_count(self):
    return User.query.filter(User.courses.contains(self)).count()

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

  @property
  def serialize(self):

    course = self.get_course()

    return {
    'id'    : self.course.id,
    'number'  : self.course.number,
    'name'    : self.course.name,
    'full_name' : repr(course).encode('ascii', 'ignore')
    }
