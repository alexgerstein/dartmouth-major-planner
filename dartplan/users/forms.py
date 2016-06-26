from flask_wtf import Form
from wtforms import TextField, IntegerField, BooleanField
from wtforms.validators import Required, NumberRange


class UserEditForm(Form):
    nickname = TextField('nickname', validators=[Required()])
    grad_year = IntegerField('Graduating Year',
                             validators=[Required(), NumberRange(min=2009,
                                                                 max=2099)])
    email_Dartplan_updates = BooleanField("DARTPlan Updates", default=True)
    email_course_updates = BooleanField("Your Planner Updates", default=True)
