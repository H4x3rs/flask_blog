#! /env python
# _*_ coding:utf8 _*_
# @author:Haojie Ren
# @time:2017/9/2 0:46

import time
from uuid import uuid4
from hashlib import sha1
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 用户表
class Users(db.Model):
    # 表名
    __tablename__ = 'users'
    # 列名
    id = db.Column(db.String(50), primary_key=True,index=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(300))
    phoneno = db.Column(db.Numeric(11))
    nickname = db.Column(db.String(300))    
    update_at = db.Column(db.TIMESTAMP(True),nullable=False)
    create_at = db.Column(db.BIGINT)
    # Establish contact with post's foreignKey:users_id
    posts = db.relationship('Posts', backref='users', lazy='dynamic')    

    # 初始化函数
    def __init__(self, email, password, phone, nickname):
        self.email = email
        self.id = str(uuid4())
        self.password = self.set_password(password)
        self.phoneno = phone
        self.nickname = nickname 
	self.create_at = int(time.time()*1000) 

    def __repr__(self):
        return "<Model User `{}`>".format(self.id)

    # 加密密码函数
    def set_password(self,password):
        pass_sha1 = sha1(password)
        return pass_sha1.hexdigest()
    
    # 检查密码正确性
    def check_password(self, password):
	pass_sha1 = sha1(password)
        return self.password == pass_sha1.hexdigest()


# posts与tags的关联表
posts_tags = db.Table(
    'posts_tags',
    db.Column('post_id', db.String(50), db.ForeignKey('posts.id')),
    db.Column('tag_id', db.String(50), db.ForeignKey('tags.id')))


# posts表
class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.String(50), primary_key=True, index=True)
    title = db.Column(db.String(100),index=True)
    content = db.Column(db.Text()) 
    update_at = db.Column(db.TIMESTAMP(True), nullable=False)
    create_at = db.Column(db.BIGINT)
    # set the foreignkey for users
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'))
    # Establish contact with Comment's ForeignKey:post_id
    comments = db.relationship('Comments', backref='posts', lazy='dynamic')
    # many to many:posts <=> tags
    tags = db.relationship('Tags', secondary=posts_tags, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, content):
        self.id = str(uuid4())
        self.title = title  
	self.content = content
        self.create_at = int(time.time()*1000)         

    def __repr__(self):
        return '<Model Posts `{}`>'.format(self.id) 

# 标签表
class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.String(50), primary_key=True, index=True)
    name = db.Column(db.String(255))
    create_at = db.Column(db.TIMESTAMP(True),nullable=False, server_default=db.text('NOW()')) 

    def __init__(self, name):
        self.name = name
	self.id =str(uuid4())

    def __repr__(self):
	return "<Model Tags `{}`>".format(self.id)


class Comments(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.String(50), primary_key=True, index=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    like = db.Column(db.INT, default=0)
    comment = db.Column(db.Text)
    create_at = db.Column(db.TIMESTAMP(True), nullable=False, server_default=db.text('NOW()'))
    pid = db.Column(db.String(50), default='0')
    # set the foreignkey for comment
    post_id = db.Column(db.String(50), db.ForeignKey('posts.id'))

    def __init__(self, name, email, comment):
        self.id = str(uuid4())
	self.name = name
	self.email = email
	self.comment = comment

    def __repr__(self):
	return '<Model Comments `{}`>'.format(self.id)
 
