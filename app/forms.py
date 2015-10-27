from flask_wtf import Form
from wtforms import StringField, BooleanField, widgets
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(Form):
	email = StringField('email', validators=[Email(), DataRequired()])
	Password = StringField('password', validators=[DataRequired()], widget=widgets.PasswordInput())
	rememberMe = BooleanField('Remember me', default=False)


class SignupForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = StringField('password', validators=[DataRequired()], widget=widgets.PasswordInput())
	password2 = StringField('password2', validators=[DataRequired(), EqualTo('password')], widget=widgets.PasswordInput())
	email = StringField('email', validators=[Email(), DataRequired()])