from flask import session
from app import db
from sqlalchemy.ext.associationproxy import association_proxy

user_course = db.Table('user_course',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
	db.Column('offering_id', db.Integer, db.ForeignKey('courses.id'))
)

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key = True)
	netid = db.Column(db.String(15), index = True, unique=True)
	full_name = db.Column(db.String(200))
	nickname = db.Column(db.String(64))
	grad_year = db.Column(db.SmallInteger)

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

	def is_taking(self, offering):
		return self.courses.filter(user_course.c.offering_id == offering.id).count() > 0

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return str(self.netid)

class Offering(db.Model):
	__tablename__ = 'courses'

	id = db.Column(db.Integer, primary_key = True)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
	term_id = db.Column(db.Integer, db.ForeignKey('term.id'))
	professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'))
	hour_id = db.Column(db.Integer, db.ForeignKey('hour.id'))

	def __repr__(self):
		return '<%r>' % (Course.query.get(int(self.course_id)))

class Course(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	number = db.Column(db.SmallInteger, unique = True)
	name = db.Column(db.String(200), index = True)

	department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
	distributive_id = db.Column(db.Integer, db.ForeignKey('distrib.id'))
	wc_id = db.Column(db.Integer, db.ForeignKey('wc.id'))

	offerings = db.relationship('Offering', backref = 'course')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '%s' % (self.name)

class Term(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	year = db.Column(db.SmallInteger)
	season = db.Column(db.String(15))
	offerings = db.relationship('Offering', backref = 'term')

	def __repr__(self):
		return '<%s%s>' % (self.year, self.season)
	
class Hour(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	period = db.Column(db.String(5), index = True, unique = True)
	offerings = db.relationship('Offering', backref = 'hour')

	def __repr__(self):
		return '<%s>' % (self.period)

class Professor(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
	name = db.Column(db.String(100), index = True, unique = True)
	
	offerings = db.relationship('Offering', backref = 'professor')

	def __repr__(self):
		return '<%s>' % (self.name)

class Department(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50), index = True, unique = True)

	courses = db.relationship('Course', backref = 'department')
	professors = db.relationship('Professor', backref = 'department')

	def __repr__(self):
		return '<%s>' % (self.name)

class Distrib(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	distributive = db.Column(db.String(4), index = True, unique = True)

	courses = db.relationship('Course', backref = 'distrib')

	def __repr__(self):
		return '<%s>' % (self.distributive)

class Wc(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	wc = db.Column(db.String(4), index = True, unique = True)

	courses = db.relationship('Course', backref = 'wc')

	def __repr__(self):
		return '<%s>' % (self.wc)
