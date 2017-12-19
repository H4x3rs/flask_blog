#! /env python
# _*_  coding:utf8 _*_
# @author:Haojie Ren

from flask import flash
from flask_wtf import FlaskForm as Form
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import Length

from flaskblog.models.users import Users

class CommentForm(Form):
    """Form validate for Comments"""
    comment = TextAreaField('comment', validators=[DataRequired(u"不能为空！"), Length(max=10000)],render_kw={"data-lenght":"1200","class":"materialize-textarea"})


class PostForm(Form):
    """Form validate for Post"""
    title = StringField('title',validators=[DataRequired(u'用户名是必须的!')])
    post = TextAreaField('post',validators=[DataRequired(u'用户名事必须的!')])
    tags = StringField('tags') 

class TagForm(object):
    code = StringField('code')
    name = StringField('name')
    pid = StringField('pid')

class LoginForm(Form):
    """Form validate for login"""
    email = StringField('email', validators=[DataRequired(u"用户名是必须的！"), Length(max=255), Email(u"无效的邮箱！")])
    password = PasswordField('password', validators=[DataRequired(u"密码是必须的！"), Length(max=255)])
    remember = BooleanField("Remember Me")

class RegisterForm(Form):
    """Form validate for register"""
    email = StringField('email', validators=[DataRequired(), Length(max=255), Email()])






# 自定义验证器
class Unique(object):
    """validate the flied is unique"""
    def __init__(self, arg):
        self.arg = arg
        

