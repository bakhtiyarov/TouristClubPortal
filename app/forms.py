from flask_wtf import Form
from wtforms import StringField, BooleanField, widgets
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
	email = StringField('email', validators=[Email(), DataRequired()])
	Password = StringField('password', validators=[DataRequired()], widget=widgets.PasswordInput())
	rememberMe = BooleanField('Remember me', default=False)