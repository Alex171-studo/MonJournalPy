
from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key= "aodnciiz@lslk17226782!!!llsjj<<>_i+"

app.permanent_session_lifetime = timedelta(days=30)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'instance','users.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
