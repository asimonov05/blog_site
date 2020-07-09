from flask import Flask

app = Flask(__name__, static_folder="static_dir")

from app import routes