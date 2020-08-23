#coding=utf-8

from flask import render_template, flash, redirect, url_for, request
from app import flask_app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

count = 0

@flask_app.route('/')
@flask_app.route('/index')
@login_required
def index():
	global count
	count += 1
	user = {}
	user['count'] = str(count)
	posts = [
		{
			'author': {'username': 'John'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'username': 'Susan'},
			'body': 'The Avengers movie was so cool!'
		}
	]
	return render_template('index.html', title='Home Page', user=user, posts=posts)

@flask_app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalide username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@flask_app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

from app import db
from app.forms import RegistrationForm
@flask_app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congradulation, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)