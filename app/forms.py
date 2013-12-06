# forms.py
# Alex Gerstein
# Client-side Forms:
# 1) Edit username/year
# 2) Select department in planner

from flask.ext.wtf import Form, TextField, IntegerField
from wtforms import TextField, IntegerField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Length, NumberRange
from app.models import Course, User, Department


class EditForm(Form):
	nickname = TextField('nickname', validators = [Required()])
	grad_year = IntegerField('Graduating Year', validators = [Required(), NumberRange(min=2009, max=2099)])

	def __init__(self, original_nickname, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.original_nickname = original_nickname

class DeptPickerForm(Form):
	dept_name = SelectField('Department', coerce=int)

	def validate(self):

		if self.dept_name.data == -1:
			return False
			
		return True

class HourPickerForm(Form):
	hour_name = SelectField('Hour', coerce=int)

	def validate(self):

		if self.hour_name.data == -1:
			return False
			
		return True

class TermPickerForm(Form):
	term_name = SelectField('Term', coerce=int)

	def validate(self):

		if self.term_name.data == -1:
			return False
			
		return True