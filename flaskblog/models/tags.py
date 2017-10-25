#! /env python
# -*- coding:utf8 -*-
# @author:ren
# @date:2017/10/25.17:32

from . import db
from uuid import uuid4

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