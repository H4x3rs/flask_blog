#! /env python
# _*_ coding:utf8 _*_
# @author:Ren
# @time:2018/3/27 21:46

from flask_wtf import FlaskForm as Form
from wtforms import StringField,TextAreaField
from wtforms.validators import DataRequired


class PostForm(Form):
    """Form validate for Post"""
    title = StringField('title',validators=[DataRequired(u'用户名是必须的!')])
    post = TextAreaField('post',validators=[DataRequired(u'用户名是必须的!')])
    tags = StringField('tags')