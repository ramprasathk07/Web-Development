from pytz import timezone
from __init__ import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    posts=db.relationship('Posts',backref='user',passive_deletes=True)
    comments=db.relationship('Comments',backref='user',passive_deletes=True)
    likes=db.relationship('Like',backref='user',passive_deletes=True)
    # follow=db.relationship('Follow',backref='user',passive_deletes=True)
    # no_of_followers = db.Column(db.Integer)
    
class Posts(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    by= db.Column(db.String(150))
    link= db.Column(db.String(900))
    desc= db.Column(db.String(900))
    date= db.Column(db.DateTime(timezone=True), default=datetime.now())
    
    title=db.Column(db.String(150))
    
    author=db.Column(db.Integer,db.ForeignKey('user.username',ondelete="CASCADE"),nullable=True)
    comments=db.relationship('Comments',backref='posts',passive_deletes=True)
    likes=db.relationship('Like',backref='posts',passive_deletes=True)    
    # follow=db.relationship('posts',backref='user',passive_deletes=True)

class Comments(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String(900))
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    post_id=db.Column(db.Integer,db.ForeignKey('posts.id',ondelete='CASCADE'),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)

class Like(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    post_id=db.Column(db.Integer,db.ForeignKey('posts.id',ondelete='CASCADE'),nullable=False)
    author=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    
class Follow(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    post_id=db.Column(db.Integer,db.ForeignKey('posts.id',ondelete='CASCADE'),nullable=False)
    author=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    follower=db.Column(db.String(100))
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    created_author=db.Column(db.String(100))
