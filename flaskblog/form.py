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

class LoginForm(Form):
    """Form validate for login"""
    email = StringField('email', validators=[DataRequired(u"用户名是必须的！"), Length(max=255), Email(u"无效的邮箱！")])
    password = PasswordField('password', validators=[DataRequired(u"密码是必须的！"), Length(max=255)])
    remember = BooleanField("Remember Me")

    def validate(self):
        check = super(LoginForm, self).validate()

        if not check:
            return False

        # check user exist
        user = Users.query.filter_by(email=self.email.data).first()
        if not user:
            flash(u'无效的用户名或密码!')
            return False

        # check password
        if not user.check_password(self.password.data):
            flash(u'无效的用户名或密码!')
            return False
        
        return True


class RegisterForm(Form):
    """Form validate for register"""
    email = StringField('email', validators=[DataRequired(), Length(max=255), Email()])
