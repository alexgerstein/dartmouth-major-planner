#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Offering, Course, Term, Department, Hour

class TestCase(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_take(self):
		u1 = User(full_name = 'Alex', netid = 'd302304')
		u2 = User(full_name = 'Santiago', netid = 'd30st04')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()

		d1 = Department(name = "Dept 1", abbr = "DEPT")
		db.session.add(d1)
		db.session.commit()

		c1 = Course(name = 'Course', number = "1", department = d1.id)
		db.session.add(c1)
		db.session.commit()

		t1 = Term(year = 2013, season = "F")
		db.session.add(t1)
		db.session.commit()

		h1 = Hour(period = "3A")
		db.session.add(h1)
		db.session.commit()

		o1 = Offering(course = c1.id, term = t1.id, hour = h1.id)
		db.session.add(o1)
		db.session.commit()

		u = u1.take(o1)
		db.session.add(u)
		db.session.commit()
		assert u1.take(o1) == None
		assert u1.is_taking(o1)

	def test_term_range(self):
		start_term = Term(year = 2013, season = "S")
		end_term = Term(year = 2014, season = "W")
		test_term1 = Term(year = 2014, season= "F")
		test_term2 = Term(year = 2013, season="F")
		test_term3 = Term(year = 2013, season = "S")
		test_term4 = Term(year = 2014, season = "W")

		old_term = Term(year = 2005, season = "W")
		db.session.add(old_term)

		db.session.add(start_term)
		db.session.add(end_term)
		db.session.add(test_term1)
		db.session.add(test_term2)
		db.session.add(test_term3)
		db.session.add(test_term4)
		db.session.commit()

		assert test_term1.in_range(start_term, end_term) == False
		assert test_term2.in_range(start_term, end_term) == True
		assert test_term3.in_range(start_term, end_term) == True
		assert test_term4.in_range(start_term, end_term) == True
		assert test_term3.in_range(old_term, test_term2) == True


if __name__ == '__main__':
	unittest.main()