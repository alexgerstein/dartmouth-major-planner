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

	terms = db.relationship("Term")


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

	def add_term(self, term):
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


	def __init__(self, course, term):
		self.course_id = course
		self.term_id = term

	def __repr__(self):
		return str((Course.query.filter_by(id = self.course_id)).first())

class Course(db.Model):
	__tablename__ = 'course'

	id = db.Column(db.Integer, primary_key = True)
	number = db.Column(db.SmallInteger)
	name = db.Column(db.String(300), index = True)

	department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
	distributive_id = db.Column(db.Integer, db.ForeignKey('distrib.id'))
	wc_id = db.Column(db.Integer, db.ForeignKey('wc.id'))

	offerings = db.relationship('Offering', backref = 'course')

	def __init__(self, number, name, department):
		self.name = name
		self.number = number
		self.department_id = department

	def offer(self, offering):
		if not self.is_offering(offering):
			self.offerings.append(offering)
			return self

	def is_offering(self, offering):
		return offering in self.offerings

	@property
	def serialize(self):
		full_name = '%s %s - %s' % (self.department.abbr, self.number, self.name)

		return {
		'full_name' :	full_name,
		'id'		:	self.id,
		'number' 	:	self.number,
		'name'		:	self.name
		}

	def __repr__(self):
		return '%s %03d - %s' % (self.department.abbr, self.number, self.name)

class Term(db.Model):
	__tablename__ = 'term'

	id = db.Column(db.Integer, primary_key = True)
	year = db.Column(db.SmallInteger)
	season = db.Column(db.String(15))

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	offerings = db.relationship('Offering', backref = 'term')

	def __init__(self, year, season):
		self.year = year
		self.season = season

	def __repr__(self):
		return '%s%s' % (str(self.year)[2:], self.season)
	
class Hour(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	period = db.Column(db.String(5), index = True, unique = True)
	offerings = db.relationship('Offering', backref = 'hour')

	def __repr__(self):
		return '<%s>' % (self.period)

class Professor(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), index = True, unique = True)
	
	offerings = db.relationship('Offering', backref = 'professor')

	def __repr__(self):
		return '<%s>' % (self.name)

class Department(db.Model):
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
	id = db.Column(db.Integer, primary_key = True)
	distributive = db.Column(db.String(4), index = True, unique = True)

	courses = db.relationship('Course', backref = 'distrib')

	def __repr__(self):
		return '%s' % (self.distributive)

class Wc(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	wc = db.Column(db.String(4), index = True, unique = True)

	courses = db.relationship('Course', backref = 'wc')

	def __repr__(self):
		return '%s' % (self.wc)
