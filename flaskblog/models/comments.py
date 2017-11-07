#! /env python
# -*- coding:utf8 -*-
# @author:ren
# @date:2017/10/25.17:32

from . import db
from uuid import uuid4

class Comments(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.String(50), primary_key=True, index=True, nullable=False)
    like = db.Column(db.INT, default=0)
    comment = db.Column(db.Text)
    create_at = db.Column(db.TIMESTAMP(True), nullable=False, server_default=db.text('NOW()'))
    pid = db.Column(db.String(50), default='0')
    # set the foreignkey for comment
    post_id = db.Column(db.String(50), db.ForeignKey('posts.id'))
    # set the foreighkey for user
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'))

    def __init__(self, name, email, comment):
        self.id = str(uuid4())
        self.comment = comment

    def __repr__(self):
        return '<Model Comments `{}`>'.format(self.id)
