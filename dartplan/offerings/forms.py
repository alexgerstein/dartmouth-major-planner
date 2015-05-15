from flask.ext.wtf import Form
from wtforms import SelectField


class DistribPickerForm(Form):
    distrib_name = SelectField('Distrib', coerce=int)


class HourPickerForm(Form):
    hour_name = SelectField('Hour', coerce=int)


class TermPickerForm(Form):
    term_name = SelectField('Term', coerce=int)
