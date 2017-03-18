# from flask.ext.wtf import Form
from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired


class PageForm(Form):
    FormTextField = StringField('FormTextField', validators=[DataRequired()])
    #remember_me = BooleanField('remember_me', default=False)
