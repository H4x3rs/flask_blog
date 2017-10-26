#! /env python
# _*_  coding:utf8 _*_
# @author:Haojie Ren

from flask_wtf import FlaskForm as Form
from wtforms import StringField
from wtforms import TextField
from wtforms import RadioField 
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import Length

from flaskblog.models.users import Users

class CommentForm(Form):
    """Form validate for Comments"""
    name = StringField('name', validators=[DataRequired("昵称是必须的"), Length(max=255, message="昵称太长了")])
    email = StringField('email', validators=[DataRequired(), Length(max=255), Email()])
    comment = TextField('comment', validators=[DataRequired(), Length(max=10000)])

class LoginForm(Form):
    """Form validate for login"""
    email = StringField('email', validators=[DataRequired(), Length(max=255), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(max=255)])
    remember = BooleanField("Remember Me")

    def validate(self):
        check = super(LoginForm, self).validate()
	
        if not check:
            return False

        # check user exist
        user = Users.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append(u'无效的用户名或密码!')
            return False

        # check password
        if not user.check_password(self.password.data):
            self.password.errors.append(u'无效的用户名或密码!')
            return False
        
        return True


class RegisterForm(Form):
    """Form validate for register"""
    email = StringField('email', validators=[DataRequired(), Length(max=255), Email()])
