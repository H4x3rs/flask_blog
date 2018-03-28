#! /env python
# _*_ coding:utf8 _*_
# @author:Ren
# @time:2018/3/27 21:45

from flask_wtf import FlaskForm as Form
from wtforms import StringField,TextAreaField,PasswordField, BooleanField
from wtforms.validators import DataRequired, Email,Length

from ..models.users import Users

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

