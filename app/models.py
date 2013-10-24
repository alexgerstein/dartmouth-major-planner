from flask import session
from app import db
from sqlalchemy.ext.associationproxy import association_proxy

SEASONS = ["W", "S", "X", "F"]


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
	off_terms = []

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
			db.session.commit()
			return self

		return None

	def drop(self, offering):
		if self.is_taking(offering):
			self.courses.remove(offering)
			db.session.commit()
			return self

		return None

	def is_enrolled(self, term):
		return term in self.terms

	def add_term(self, term):
		if not self.is_enrolled(term):
			self.terms.append(term)
			return self
	
	def remove_term(self, term):
		self.terms.remove(term)
		return self

	def swap_onterm(self, term):
		if self.is_enrolled(term):
			if self.is_on(term):
				self.off_terms.append(str(term))
			else:
				self.off_terms.remove(str(term))
			return self


	def is_taking(self, offering):
		return self.courses.filter(user_course.c.offering_id == offering.id).count() > 0

	def is_on(self, term):
		for off_term in self.off_terms:
			if str(term) == str(off_term):
				return False

		return True

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return str(self.netid)

class Offering(db.Model):
	__tablename__ = 'offering'

	id = db.Column(db.Integer, primary_key = True)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
	term_id = db.Column(db.Integer, db.ForeignKey('term.id'))
	hour_id = db.Column(db.Integer, db.ForeignKey('hour.id'))
	desc = db.Column(db.String(25000))

	# distributives = db.relationship("Distrib", backref="offering")
	# wc_id = db.Column(db.Integer, db.ForeignKey('wc.id'))

	added = db.Column(db.String(2))
	user_added = db.Column(db.String(2))

	def __init__(self, course, term, hour, desc, user_added):
		self.course_id = course
		self.term_id = term
		self.hour_id = hour
		self.desc = desc
		self.user_added = user_added
		# self.wc_id = wc

		# for distrib in distribs:
		# 	self.distributives.append(distrib)

	def get_full_name(self):
		return str(Course.query.filter_by(id = self.course_id).first())

	def get_term(self):
		return Term.query.filter_by(id = self.term_id).first()

	def mark(self, str):
		self.added = str
		return self

	def mark_empty(self):
		self.added = ""
		return self

	def mark_user_added(self):
		self.user_added = "Y"
		return self

	def __repr__(self):
		course = Course.query.filter_by(id = self.course_id).first()
		hour = Hour.query.filter_by(id = self.hour_id).first()

		return "%s %s (%s)" % (course.department.abbr, course.number, hour)

class Course(db.Model):
	__tablename__ = 'course'

	id = db.Column(db.Integer, primary_key = True)
	number = db.Column(db.String(10, convert_unicode = True))
	name = db.Column(db.String(300), index = True)

	department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

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

		return {
		'full_name' :	repr(self).encode('ascii', 'ignore'),
		'id'		:	self.id,
		'number' 	:	self.number,
		'name'		:	self.name
		}

	def __repr__(self):
		department = Department.query.filter_by(id = self.department_id).first()

		return '%s %s - %s' % (department.abbr, self.number, self.name.encode('ascii', 'ignore'))

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
	period = db.Column(db.String(50), index = True, unique = True)
	offerings = db.relationship('Offering', backref = 'hour')

	def __init__(self, period):
		self.period = period

	def __repr__(self):
		if (self.period == "Arrange"):
			return 'Arr'

		return '%s' % (self.period)

class Department(db.Model):
	__tablename__ = "department"

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), index = True, unique = True)
	abbr = db.Column(db.String(10), index = True, unique = True)

	courses = db.relationship('Course', backref = 'department')

	def __init__(self, name, abbr):
		self.name = name
		self.abbr = abbr

	def __repr__(self):
		return '%s' % (self.abbr)
