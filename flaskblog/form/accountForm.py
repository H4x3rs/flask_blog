#! /env python
# _*_ coding:utf8 _*_
# @author:Ren
# @time:2018/4/1 19:37


import re
from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from ..models.users import Users

__all__ = ['LoginForm', 'RegisterForm']


class LoginForm(Form):
    """Form validate for login"""
    email = StringField('email', validators=[DataRequired(u"用户名是必须的！"), Length(max=255), Email(u"无效的邮箱！")])
    password = PasswordField('password', validators=[DataRequired(u"密码是必须的！"), Length(max=255)])
    remember = BooleanField("Remember Me")

    def validate(self):
        """Validator for check the account information"""
        check_validate = super(LoginForm, self).validate()

        if not check_validate:
            return False

        user = Users.query.filter_by(email=self.email.data).first()
        # check user email whether right
        if not user:
            self.email.errors.append(u'无效的用户名或密码！')
            return False
        # check user password whether right
        if not user.check_password(self.password.data):
            self.email.errors.append(u'无效的用户名和密码！')
            return False

        return True


class RegisterForm(Form):
    nickname = StringField('nickname', validators=[DataRequired(u"昵称是必须的！"), Length(max=30)])
    email = StringField('email', validators=[DataRequired(u"用户名是必须的！"), Length(max=255), Email(u"无效的邮箱！")])
    password = PasswordField('password',
                             validators=[DataRequired(u"密码是必须的！"), Length(6, 16, message=u"密码必须为6-16为数字、字母组合")])
    confirm = PasswordField('confirm',
                            validators=[DataRequired(u'请重复一次密码！'), Length(6, 16, message=u"密码必须为6-16为数字、字母组合")])

    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        if not check_validate:
            return False

        user = Users.query.filter_by(email=self.email.data).first()

        if user:
            self.email.errors.append(u"该用户名已存在！")
            return False

        if self.password.data != self.confirm.data:
            print("两次输入密码不一致")
            self.confirm.errors.append(u"两次输入密码不一致！")
            return False

        # if len(self.password.data)< 6 or len(self.password.data)>16:
        #     self.password.errors.append(u"密码必须为6-16位字符、数字")
        #     return False

        if not re.search("^(?![A-Z]+$)(?![a-z]+$)(?!\d+$)(?![\W_]+$)\S{6,16}$", self.password.data):
            self.password.errors.append(u"密码必须为6-16位数字、字母组合")
            return False

        return True
