from app import app, db
from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app.models import Post, User
from app.forms import PostForm, ResetPasswordRequestForm, RegistrationForm, EmptyForm, LoginForm, ResetPasswordForm
from app.email import send_email, send_password_reset_email

@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()


@app.route('/')
@app.route('/index')
def index():
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	print(posts)
	return render_template('index.html', posts=posts, current_user=current_user)

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

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash(f'Письмо с дальнейшей инструкцией отправлено на почту {user.email}')
		return redirect(url_for('login'))
	return render_template('reset_pass.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_1(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Ваш пароль успешно изменен.')
		return redirect(url_for('login'))
	return render_template('reset_password.html', form=form)


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
	return render_template("new_post.html", form=form)


@app.route('/post/<post_id>')
def post(post_id):
	post = Post.query.filter_by(id=post_id).first_or_404()
	form = EmptyForm()
	if current_user.is_authenticated:
		user = current_user.username
	else:
		user = ""
	return render_template('post.html', post=post, form=form, user=user)

@app.route('/post/delete/<id>', methods=['GET', 'POST'])
def delete_post(id):
	post_auth = db.session.query(Post.id, User.username).join(Post).filter_by(id=id).first_or_404()
	print(post_auth)
	if post_auth.username == current_user.username:
		post = Post.query.filter_by(id=id).first()
		db.session.delete(post)
		db.session.commit()
		flash('Ваш пост успешно удален!')
	return redirect(url_for('index'))


@app.route('/user/<username>')
def user(username):
	post_user = Post.query.join(User).filter_by(username=username).order_by(Post.timestamp.desc()).all()
	user = db.session.query(User.username, User.last_seen).filter_by(username=username).first()
	return render_template('user.html', user=user, post=post_user)