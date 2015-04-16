from flask.ext.wtf import Form
from wtforms import SelectField


class DistribPickerForm(Form):
    distrib_name = SelectField('Distrib', coerce=int)

    def validate(self):

        if self.distrib_name.data == -1:
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
