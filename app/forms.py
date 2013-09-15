from flask.ext.wtf import Form, TextField, IntegerField
from wtforms import TextField, IntegerField
from wtforms.validators import Required, Length, NumberRange
from app.models import User


class EditForm(Form):
	nickname = TextField('nickname', validators = [Required()])
	grad_year = IntegerField('Graduating Year', validators = [Required(), NumberRange(min=2000, max=2040)])

	def __init__(self, original_nickname, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.original_nickname = original_nickname