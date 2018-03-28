#! /env python
# _*_ coding:utf8 _*_
# @author:Ren
# @time:2018/3/27 21:45

from flask_wtf import FlaskForm as Form
from wtforms import StringField,TextAreaField
from wtforms.validators import DataRequired,Length


class CommentForm(Form):
    """Form validate for Comments"""
    comment = TextAreaField('comment', validators=[DataRequired(u"不能为空！"), Length(max=10000)],render_kw={"data-lenght":"1200","class":"materialize-textarea"})
