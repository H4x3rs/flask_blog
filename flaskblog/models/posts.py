#! /env python
# -*- coding:utf8 -*-
# @author:ren
# @date:2017/10/25.17:32

import time
from . import db
from uuid import uuid4
from .posts_tags import posts_tags

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