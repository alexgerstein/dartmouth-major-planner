#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Offering, Course

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

		c1 = Course(name = 'Course 1')
		db.session.add(c1)
		db.session.commit()

		o1 = Offering(course = c1)
		db.session.add(o1)
		db.session.commit()

		u = u1.take(o1)
		db.session.add(u)
		db.session.commit()
		assert u1.take(o1) == None
		assert u1.is_taking(o1)

if __name__ == '__main__':
	unittest.main()