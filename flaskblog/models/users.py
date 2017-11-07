#! /env python
# -*- coding:utf8 -*-
# @author:ren
# @date:2017/10/25.17:32

import time
from uuid import uuid4
from hashlib import sha1
from flaskblog.models import db
from flask_login import AnonymousUserMixin

# 用户表
class Users(db.Model):
    # 表名
    __tablename__ = 'users'
    # 列名
    id = db.Column(db.String(50), primary_key=True, index=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(300))
    phoneno = db.Column(db.Numeric(11))
    nickname = db.Column(db.String(300))
    status = db.Column(db.INT)
    update_at = db.Column(db.TIMESTAMP(True), nullable=False)
    create_at = db.Column(db.BIGINT)
    # Establish contact with post's foreignKey:users_id
    posts = db.relationship('Posts', backref='users', lazy='dynamic')
    # Establish contact with comments's foreignKey:users_id
    comments = db.relationship('Comments', backref='users', lazy='dynamic')

    # 初始化函数
    def __init__(self, email, password, phone, nickname):
        self.email = email
        self.id = str(uuid4())
        self.password = self.set_password(password)
        self.phoneno = phone
        self.nickname = nickname
        self.create_at = int(time.time() * 1000)

    # 加密密码函数
    def set_password(self, password):
        pass_sha1 = sha1(password)
        return pass_sha1.hexdigest()

    # 检查密码正确性
    def check_password(self, password):
        pass_sha1 = sha1(password)
        return self.password == pass_sha1.hexdigest()

    # 检查用户是否登录
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True
    # 检查用户是否激活
    def is_active(self):
        if self.status == 1:
            return True
        else:
            return False
    # 检查是否是匿名用户
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True
    # 返回用户ID
    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return "<Model User `{}`>".format(self.id)
