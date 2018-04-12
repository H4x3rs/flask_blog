#! /env python
# -*- coding:utf8 -*-
# @author:ren
# @date:2017/10/25.17:32

import timeit
from .db import db
from uuid import uuid4


class Roles(db.Model):
    '''Represents Prroected Roles '''
    __tablename__ = 'roles'

    id = db.Column(db.String(50), primary_key=True)
    role = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, role):
        self.id = str(uuid4())
        self.role = role

    def __repr__(self):
        return "<Model Role `{}`>".format(self.id)
