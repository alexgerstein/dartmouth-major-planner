from flask.ext.wtf import Form, TextField, IntegerField
from wtforms import TextField, IntegerField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Length, NumberRange
from app.models import Course, User, Department


class EditForm(Form):
	nickname = TextField('nickname', validators = [Required()])
	grad_year = IntegerField('Graduating Year', validators = [Required(), NumberRange(min=2000, max=2040)])

	def __init__(self, original_nickname, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.original_nickname = original_nickname

class DeptForm(Form):
	dept_name = QuerySelectField('Department', query_factory=Department.query.all, allow_blank=True)
	course_name = QuerySelectField('Course', allow_blank=True)