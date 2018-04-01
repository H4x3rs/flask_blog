#! /env python
# _*_ coding:utf8 _*_
# @author:Ren
# @time:2018/3/27 21:46

from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

__all__ = ['PostForm', 'TagForm', 'CommentForm']


class PostForm(Form):
    """Form validate for Post"""
    title = StringField('title', validators=[DataRequired(u'标题不能为空!')])
    post = TextAreaField('post', validators=[DataRequired(u'内容不能为空!')])
    tags = StringField('tags')


class TagForm(object):
    code = StringField('code')
    name = StringField('name')
    pid = StringField('pid')


class CommentForm(Form):
    """Form validate for Comments"""
    comment = TextAreaField('comment', validators=[DataRequired(u"不能为空！"), Length(max=10000)],
                            render_kw={"data-lenght": "1200", "class": "materialize-textarea"})
