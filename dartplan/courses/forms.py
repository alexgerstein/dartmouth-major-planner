from flask.ext.wtf import Form
from wtforms import SelectField


class DeptPickerForm(Form):
    dept_name = SelectField('Department', coerce=int)


class MedianPickerForm(Form):
    median_name = SelectField('Median', coerce=int)
