from flask import session
from app import db
from sqlalchemy.ext.associationproxy import association_proxy

user_course = db.Table('user_course',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('offering_id', db.Integer, db.ForeignKey('offering.id'))
)

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key = True)
	netid = db.Column(db.String(15), index = True, unique=True)
	full_name = db.Column(db.String(200))
	nickname = db.Column(db.String(64))
	grad_year = db.Column(db.SmallInteger)

	terms = db.relationship("Term", backref = "user", lazy='dynamic')


	courses = db.relationship('Offering', 
		secondary=user_course,
		backref=db.backref('users', lazy = 'dynamic'),
		lazy = 'dynamic')

	def __init__(self, full_name, netid):
		self.full_name = full_name
		self.netid = netid
		self.nickname = full_name

	def email(self):
		return "%s@dartmouth.edu" % self.netid

	def take(self, offering):
		if not self.is_taking(offering):
			self.courses.append(offering)
			return self

		return None

	def drop(self, offering):
		if self.is_taking(offering):
			self.courses.remove(offering)
			return self

	def is_enrolled(self, term):
		return term in self.terms

	def add_term(self, term):
		if not self.is_enrolled(term):
			self.terms.append(term)
			return self
	
	def remove_term(self, term):
		self.terms.remove(term)
		return self


	def is_taking(self, offering):
		return self.courses.filter(user_course.c.offering_id == offering.id).count() > 0

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return str(self.netid)

class Offering(db.Model):
	__tablename__ = 'offering'

	id = db.Column(db.Integer, primary_key = True)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
	term_id = db.Column(db.Integer, db.ForeignKey('term.id'))
	professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'))
	hour_id = db.Column(db.Integer, db.ForeignKey('hour.id'))

	def __init__(self, course, term, hour):
		self.course_id = course
		self.term_id = term
		self.hour_id = hour

	def get_full_name(self):
		return str(Course.query.filter_by(id = self.course_id).first())

	def __repr__(self):
		course = Course.query.filter_by(id = self.course_id).first()

		return "%s %s (%s)" % (course.department.abbr, course.number, self.hour)

class Course(db.Model):
	__tablename__ = 'course'

	id = db.Column(db.Integer, primary_key = True)
	number = db.Column(db.SmallInteger)
	name = db.Column(db.String(300), index = True)

	department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
	distributives = db.relationship("Distrib", backref="course")
	wc_id = db.Column(db.Integer, db.ForeignKey('wc.id'))

	offerings = db.relationship('Offering', backref = 'course')

	def __init__(self, number, name, department, distribs, wc):
		self.name = name
		self.number = number
		self.department_id = department

		self.wc_id = wc
		for distrib in distribs:
			self.distributives.append(distrib)

	def offer(self, offering):
		if not self.is_offering(offering):
			self.offerings.append(offering)
			return self

	def is_offering(self, offering):
		return offering in self.offerings

	@property
	def serialize(self):
		return {
		'full_name' :	str(self),
		'id'		:	self.id,
		'number' 	:	self.number,
		'name'		:	self.name
		}

	def __repr__(self):
		department = Department.query.filter_by(id = self.department_id).first()


		return '%s %s - %s' % (department.abbr, self.number, self.name)

class Term(db.Model):
	__tablename__ = 'term'

	id = db.Column(db.Integer, primary_key = True)
	year = db.Column(db.SmallInteger)
	season = db.Column(db.String(15))

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	offerings = db.relationship('Offering', backref = 'term', lazy='dynamic')

	def __init__(self, year, season):
		self.year = year
		self.season = season

	@property
	def serialize(self):
		return {
		'term' :	str(self.year)[2:] + self.season
		}

	def __repr__(self):
		return '%s%s' % (str(self.year)[2:], self.season)
	
class Hour(db.Model):
	__tablename__ = "hour"

	id = db.Column(db.Integer, primary_key = True)
	period = db.Column(db.String(5), index = True, unique = True)
	offerings = db.relationship('Offering', backref = 'hour')

	def __init__(self, period):
		self.period = period

	def __repr__(self):
		if (self.period == "Arrange"):
			return 'Arr'

		return '%s' % (self.period)

class Professor(db.Model):
	__tablename__ = "professor"

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), index = True, unique = True)
	
	offerings = db.relationship('Offering', backref = 'professor')

	def __repr__(self):
		return '<%s>' % (self.name)

class Department(db.Model):
	__tablename__ = "department"

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50), index = True, unique = True)
	abbr = db.Column(db.String(10), index = True, unique = True)

	courses = db.relationship('Course', backref = 'department')

	def __init__(self, name, abbr):
		self.name = name
		self.abbr = abbr

	def __repr__(self):
		return '%s' % (self.abbr)

class Distrib(db.Model):
	__tablename__ = "distrib"

	id = db.Column(db.Integer, primary_key = True)
	distributive = db.Column(db.String(4), index = True, unique = True)

	parent_id = db.Column(db.Integer, db.ForeignKey('course.id'))

	def __init__(self, abbr):
		self.distributive = abbr

	def __repr__(self):
		return '%s' % (self.distributive)

class Wc(db.Model):
	__tablename__ = "wc"

	id = db.Column(db.Integer, primary_key = True)
	wc = db.Column(db.String(4), index = True, unique = True)

	courses = db.relationship('Course', backref = 'wc')

	def __init__(self, abbr):
		self.wc = abbr

	def __repr__(self):
		return '%s' % (self.wc)
