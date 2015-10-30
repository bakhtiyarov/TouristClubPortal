from flask_wtf import Form
from wtforms import StringField, BooleanField, widgets, TextAreaField
import wtforms.ext.dateutil
from wtforms.ext.dateutil.fields import DateField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, Optional, URL
from app.models import PassportData
import re


class LoginForm(Form):
	email = StringField('email', validators=[Email(), DataRequired()])
	Password = StringField('password', validators=[DataRequired()], widget=widgets.PasswordInput())
	rememberMe = BooleanField('Remember me', default=False)


class SignupForm(Form):
	first_name = StringField('first_name', validators=[DataRequired()])
	second_name = StringField('second_name')
	patronymic = StringField('patronymic')
	password = StringField('password', validators=[DataRequired()], widget=widgets.PasswordInput())
	password2 = StringField('password2', validators=[DataRequired(), EqualTo('password')], widget=widgets.PasswordInput())
	email = StringField('email', validators=[Email(), DataRequired()])


#TODO: move Regexps into config.py - admin of portal can setup correct phone number and passport number format
class EditPassportDataForm(Form):
	first_name = StringField('first_name')
	second_name = StringField('second_name')
	patronymic  = StringField('patronymic')

	ser = StringField('passport_ser', validators=[Regexp('[A-Z]{2}', flags=re.IGNORECASE), Optional()])
	num = StringField('passport_num', validators=[Regexp('[0-9]+'), Optional()])
	issue_date = DateField('passport_issue_date', validators=[Optional()])
	expire_date = DateField('passport_expire_date', validators=[Optional()])
	issuer = StringField('issuer')
	address = TextAreaField('address')

	birthdata = DateField('birthday', validators=[Optional()])
	mobile_phone = StringField('mobile_phone', validators=[Regexp('[\+0-9]*')])
	additional_phone = StringField('additional_phone', validators=[Regexp('[\+0-9]*')])
	work_phone = StringField('work_phone', validators=[Regexp('[\+0-9]*')])
	home_phone = StringField('home_phone', validators=[Regexp('[\+0-9]*')])

	second_email = StringField('second_email', validators=[Email(), Optional()])
	skype_account = StringField('skype_account')
	facebook_account = StringField('facebook_account', validators=[URL(), Optional()])
	vk_account = StringField('vk_account', validators=[URL(), Optional()])

	work_place = TextAreaField('work_place')


def setForm(form, data):
	"""
	:type data: PassportData
	"""
	form.first_name.data = data.first_name
	form.second_name.data = data.second_name
	form.patronymic.data = data.patronymic
	form.ser.data = data.ser
	form.num.data = data.num
	form.issuer.data = data.issuer
	form.issue_date.data = data.issue_date
	form.expire_date.data = data.release_date
	form.address.data = data.address
	form.birthdata.data = data.birthday
	form.mobile_phone.data = data.mobile_phone
	form.additional_phone.data = data.additional_phone
	form.work_phone.data = data.work_phone
	form.home_phone.data = data.home_phone
	form.second_email.data = data.second_email
	form.skype_account.data = data.skype_account
	form.facebook_account.data = data.facebook_account
	form.vk_account.data = data.vk_account
	form.work_place.data = data.work_place