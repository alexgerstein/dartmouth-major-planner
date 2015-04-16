from flask.ext.wtf import Form
from wtforms import TextField, IntegerField, BooleanField
from wtforms.validators import Required, NumberRange


class UserEditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    grad_year = IntegerField('Graduating Year', validators = [Required(), NumberRange(min=2009, max=2099)])
    dartplan_updates = BooleanField("DARTPlan Updates", default = True)
    course_updates = BooleanField("Your Planner Updates", default = True)

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname
