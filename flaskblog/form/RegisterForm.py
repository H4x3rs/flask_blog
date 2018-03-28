#! /env python
# _*_ coding:utf8 _*_
# @author:Ren
# @time:2018/3/27 21:45

from ..models.users import Users
from flask_wtf import Form
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterForm(Form):
    email = StringField('email', validators=[DataRequired(u"用户名是必须的！"), Length(max=255), Email(u"无效的邮箱！")])
    password = PasswordField('password', validators=[DataRequired(u"密码是必须的！"), Length(max=255,min=6)])
    comfirm = PasswordField('comfirm password',[DataRequired(u'请重复一次密码！'),EqualTo('password')])

    def validate(self):
        check_validate = super(RegisterForm,self).validate()

        if not check_validate:
            return False

        user = Users.query.filter_by(email = self.email.data).first()

        if user:
            self.email.errors.append(u"该用户名已存在！")
            return False

        return True






































