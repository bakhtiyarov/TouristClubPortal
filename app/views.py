from wtforms.validators import email
from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g, abort, send_file
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, SignupForm, EditPassportDataForm, setForm
from app.models import User, ROLE_ADMIN, ROLE_USER, ROLE_LEADER, STATUS_BANNED, STATUS_OK, STATUS_READ_ONLY
from app.models import PassportData
import bcrypt
from hashlib import md5
from wand.image import Image
from config import UPLOADED_AVATARS_DEST, basedir
from os import path
import io


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.route('/')
@app.route('/index')
@login_required
def index():
	current_user = g.user
	last_messages = [
		{
			'author': {'first_name': 'Linus Torvalds'},
			'message': 'It is a stupid microblog service!',
			'date' : '2015.10.11'
		},
		{
			'author': {'first_name': 'Ed Musheed'},
			'message': "It's a very poor design. May be you need another HTML/CSS programmer? :)",
			'date' : '2015.10.10'
		}
	]
	return render_template('index.html', title="Home page", user=current_user, messages=last_messages, authenticated=True)


@app.route('/downloads')
def downs():
	return "There is no available downloads yet!"


@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('/index'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).one_or_none()
		password = form.Password.data
		if user is not None:
			if bcrypt.checkpw(form.Password.data, user.password):
				session["rememberMe"] = form.rememberMe.data
				login_user(user, form.rememberMe.data)
				return redirect(request.args.get('next') or url_for('index') )
		else:
			return redirect(url_for('login'))

	return render_template('login.html', title='Sign In', form=form, authenticated=False)


@app.before_request
def before_request():
	g.user = current_user


@lm.user_loader
def load_user(id):
	return User.query.get(id)


@login_required
@app.route('/logout')
def logout():
	user = current_user
	logout_user()
	return redirect(request.args.get('next') or url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		userlist = User.query.filter_by(email = form.email.data)
		if userlist.count() > 0:
			print("Can't signup user with already existing e-mail " + form.email.data + '!')
			flash( "Can't register you because this e-mail already registered!" )
			return redirect( '/signup' )

		user = User(form.first_name.data, form.second_name.data, form.patronymic.data, form.email.data,
					form.password.data, ROLE_USER, STATUS_READ_ONLY)
		db.session.add(user)
		db.session.commit()
		flash('Your registration has finished! You can login using your e-mail address and password')
		return redirect('/')

	return render_template('signup.html', completed=False, form=form, authenticated=False)


@app.route('/profile/<user_id>')
@login_required
def profile(user_id):
	user = load_user(user_id)
	if (user == current_user or user.in_one_group_with(current_user) or current_user.role == ROLE_ADMIN) and user.passport_data is not None:
		pd = PassportData.query.get(user.passport_data)
		return render_template('contactsData.html', editable=(user == current_user), data=user, authenticated=True, passport=pd, passport_allowed=True)
	else:
		return render_template('contactsData.html', editable=(user == current_user), data=user, authenticated=True, passport_allowed=False)


@app.route('/profile')
@login_required
def redirect_to_profile():
	return redirect('/profile/' + str(current_user.id))


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	user = current_user
	if user.passport_data is None:
		pd = PassportData(user.id)
		db.session.add(pd)
		db.session.commit()
		user.passport_data = pd.id
		db.session.commit()
	cur_data = PassportData.query.get(user.passport_data)
	if cur_data is None:
		cur_data = PassportData()
	form = EditPassportDataForm()
	if form.validate_on_submit():
		if cur_data is None:
			db.session.add(cur_data)


		#TODO: is it available to process only modified values?
		cur_data.first_name = form.first_name.data
		cur_data.second_name = form.second_name.data
		cur_data.patronymic = form.patronymic.data
		cur_data.birthday = form.birthdata.data
		cur_data.ser = form.ser.data
		cur_data.num = form.num.data
		cur_data.mobile_phone = form.mobile_phone.data
		cur_data.additional_phone = form.additional_phone.data
		cur_data.work_phone = form.work_phone.data
		cur_data.home_phone = form.home_phone.data
		cur_data.second_email = form.second_email.data
		cur_data.skype_account = form.skype_account.data
		cur_data.facebook_account = form.facebook_account.data
		cur_data.vk_account = form.vk_account.data
		cur_data.issue_date = form.issue_date.data
		cur_data.issuer = form.issuer.data
		cur_data.release_date = form.expire_date.data
		cur_data.address = form.address.data
		cur_data.work_place = form.work_place.data

		db.session.add(cur_data)
		db.session.commit()
		return redirect('/profile')

	else:
		setForm(form, cur_data)
		return render_template('edit_profile.html', data=user, authenticated=True, form=form)


@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
	#TODO: process situation when request.files don't have needed file
	if request.method == 'POST' and 'userFile' in request.files:
		hasher = md5()
		hasher.update(current_user.email.encode('utf-8'))
		f1 = request.files['userFile']
		filename = path.join(UPLOADED_AVATARS_DEST, hasher.hexdigest())
		f1.save(filename)
		print('new avatar for user ' + current_user.first_name + current_user.second_name + ' was saved as ' + filename)
		img = Image(filename=filename)
		if img is None:
			print("Can't parse blob from post message as image!")
			return redirect('/profile')
		else:
			img.resize(320, 240)
			img = img.convert('png')
			user = current_user
			user.load_avatar(img)
			return redirect('/profile')
	else:
		#TODO: redirect to previous url
		return redirect('/')


@app.route('/avatar/<user_id>')
def get_avatar(user_id):
	user = load_user(user_id)
	if user is None:
		abort(404)
	else:
		if user.avatar is None:
			filename = path.join('app', 'static', 'no_avatar.png')
			return send_file(filename)
		else:
			return send_file(io.BytesIO(user.avatar), mimetype='image/png')

@login_required
@app.route('/avatar')
def get_my_avatar():
	user = current_user
	return redirect('/avatar/' + str(user.id))