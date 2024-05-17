from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
db=SQLAlchemy()
class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False,index=True)
    email = db.Column(db.String(120), unique=True, nullable=False,index=True)
    password = db.Column(db.String(256))
    money=db.Column(db.Integer,default=0)
    photopath=db.Column(db.String(120),nullable=False,default='default.png')
class Article(db.Model):
    __tablename__='article'
    id=db.Column(db.Integer,primary_key=True)
    userid=db.Column(db.Integer,db.ForeignKey('user.id'))
    title=db.Column(db.String(120),nullable=False)
    content=db.Column(db.String(500),nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now())
    user = db.relationship('User', backref=db.backref('article', lazy=True))
class Comment(db.Model):
    __tablename__='comment'
    id=db.Column(db.Integer,primary_key=True)
    articleid=db.Column(db.Integer,db.ForeignKey('article.id'))
    userid=db.Column(db.Integer,db.ForeignKey('user.id'))
    content=db.Column(db.String(120),nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now())
    article=db.relationship('Article', backref=db.backref('comment', lazy=True))
    user= db.relationship('User', backref=db.backref('comment', lazy=True))
class Articlelike(db.Model):
    __tablename__='articlelike'
    id=db.Column(db.Integer,primary_key=True)
    articleid=db.Column(db.Integer,db.ForeignKey('article.id'))
    userid=db.Column(db.Integer,db.ForeignKey('user.id'))
    status=db.Column(db.Boolean,default=True)
    create_time=db.Column(db.DateTime,default=datetime.now())
    article=db.relationship('Article', backref=db.backref('articlelike', lazy=True))
    user= db.relationship('User', backref=db.backref('articlelike', lazy=True))