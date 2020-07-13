import os
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class Config(object):
	UPLOAD_FOLDER = '/app/'
	ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'the_most_difficult_password_'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False