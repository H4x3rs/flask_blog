#! /env python
# _*_ coding:utf8 _*_
# @author:Ren
# @time:2018/3/27 21:45

from wtforms import StringField


class TagForm(object):
    code = StringField('code')
    name = StringField('name')
    pid = StringField('pid')