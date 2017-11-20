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
    code = db.Column(db.String(255))
    name = db.Column(db.String(255))
    create_at = db.Column(db.TIMESTAMP(True),nullable=False, server_default=db.text('NOW()'))
    pid = db.Column(db.String(50))

    def __init__(self, name, code=None, pid=None):
        self.name = name
        self.pid = pid
        self.id =str(uuid4())
        if code == None:
	    self.code = self.name
        else:
	    self.code = code

    def __repr__(self):
        return "<Model Tags `{}`>".format(self.id)
