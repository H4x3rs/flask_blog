#! /env python
# -*- coding:utf8 -*-
# @author:ren
# @date:2017/10/25.17:32

from datetime import datetime
from uuid import uuid4
from hashlib import sha1
from .db import db
from .users_roles import users_roles
from .roles import Roles

from flask_login import AnonymousUserMixin


# 用户表
class Users(db.Model):
    # 表名
    __tablename__ = 'users'
    # 列名
    id = db.Column(db.String(50), primary_key=True, index=True)
    email = db.Column(db.String(100), unique=True)
    passwd = db.Column(db.String(300))
    phoneno = db.Column(db.Numeric(11))
    nickname = db.Column(db.String(200))
    status = db.Column(db.INT)
    update_at = db.Column(db.TIMESTAMP(True), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow,)
    head_pic = db.Column(db.String(255))
    # Establish contact with post's foreignKey:users_id
    posts = db.relationship('Posts', backref='users', lazy='dynamic')
    # Establish contact with comments's foreignKey:users_id
    comments = db.relationship('Comments', backref='users', lazy='dynamic')
    # Establish contact with role's foreignKey:users_id
    roles = db.relationship('Roles', secondary=users_roles, backref='users', lazy='dynamic')

    # 初始化函数
    def __init__(self, email, nickname):
        self.email = email
        self.id = str(uuid4())
        self.nickname = nickname
        self.status = 0

        # setup the default role for user
        default = Roles.query.filter_by(role == 'default').one()
        self.roles.append(default)

    # get/set status
    @property
    def status(self):
        if self.status == 0:
            return "status: not active/未激活！"
        if self.status == 1:
            return "status: yet active/已激活！"

    @status.setter
    def status(self, status):
        self._status = status

    # set/get password
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        pass_hash = sha1(password.encode('utf8'))
        self.passwd = pass_hash.hexdigest()

    # # 加密密码函数
    # def set_password(self, password):
    #     pass_sha1 = sha1(password)
    #     return pass_sha1.hexdigest()

    # 检查密码正确性
    def check_password(self, password):
        pass_sha1 = sha1(password.encode('utf8'))
        return self.passwd == pass_sha1.hexdigest()

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
        return self.id

    def __repr__(self):
        return "<Model User `{}`>".format(self.id)
