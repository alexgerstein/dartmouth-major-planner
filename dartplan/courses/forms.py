from flask.ext.wtf import Form
from wtforms import SelectField


class DeptPickerForm(Form):
    dept_name = SelectField('Department', coerce=int)

    def validate(self):

        if self.dept_name.data == -1:
            return False

        return True


class MedianPickerForm(Form):
    median_name = SelectField('Median', coerce=int)

    def validate(self):

        if self.median_name.data == -1:
            return False

        return True
