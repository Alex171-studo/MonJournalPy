from flask_sqlalchemy import SQLAlchemy
from config import db
from werkzeug.security import generate_password_hash, check_password_hash
from babel import Locale
from babel.dates import format_datetime
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),unique= True)
    email = db.Column(db.String(120),nullable = False,unique = True)
    password_hash = db.Column(db.String(128),nullable = False)
    
    posts =db.relationship("Post",backref='author',lazy=True)
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
        
class Post(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    content = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime,nullable= False, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
    def __repr__(self):
        return f"Post '{self.title}', ID: '{self.id}', UserID:'{self.user_id}' "