from app import app, db
from flask import render_template, redirect, flash, url_for, request
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
from datetime import datetime
from app.models import Post
from app.forms import PostForm

@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()


posts = [
	"«Ростелеком» заподозрил школьников в DDoS-атаках на учебные ресурс"] * 21

@app.route('/')
@app.route('/index')
def index():
	global posts
	return render_template('index.html', posts=posts)

@app.route('/themes')
def themes():
	return render_template('themes.html')

@app.route('/subs')
@login_required
def subs():
	return render_template('subs.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if not(user is None):
			if user.check_password(form.password.data):
				login_user(user, remember=form.remember_me.data)
				next_page = request.args.get('next')
				if not next_page or url_parse(next_page).netloc != '':
					next_page = url_for('index')
				return redirect(next_page)
			else:
				flash('Неверный пароль')
		else:
			flash('Неверный логин')
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.post_title.data,body=form.post.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template("index.html", form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def not_found_error(error):
    return render_template('500.html'), 500