from app import app
from flask import render_template

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
def subs():
	return render_template('subs.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def not_found_error(error):
    return render_template('500.html'), 500