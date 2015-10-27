from wtforms.validators import email
from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm
from app.models import User, ROLE_ADMIN, ROLE_USER, ROLE_LEADER
import bcrypt


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
			'author': {'nickname': 'Linus Torvalds'},
			'message': 'It is a stupid microblog service!',
			'date' : '2015.10.11'
		},
		{
			'author': {'nickname': 'Ed Musheed'},
			'message': "It's a very poor design. May be you need another HTML/CSS programmer? :)",
			'date' : '2015.10.10'
		}
	]
	return render_template('index.html', title="Home page", user=current_user, messages=last_messages)


@app.route('/downloads')
def downs():
	return "There is no available downloads yet!"


@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('/index'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data)[0]
		password = form.Password.data
		if user is not None:
			if bcrypt.checkpw(form.Password.data, user.password):
				session["rememberMe"] = form.rememberMe.data
				login_user(user, form.rememberMe.data)
				return redirect(request.args.get('next') or url_for('index') )
		else:
			return redirect(url_for('login'))

	return render_template('login.html', title='Sign In', form=form)


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
	return redirect(url_for('index'))