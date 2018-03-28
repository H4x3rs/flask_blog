#! /env python
# -*- coding:utf8 -*-
# @author:ren
# @date:2018/3/22.16:41

from flask.views import MethodView
from flask import url_for, flash, redirect, render_template
from ...form import LoginForm


# login、logout、facebook、QQ、weixin、github、google

def login(email, password, back=url_for("blog.index")):
    form = LoginForm()
    if form.validate_on_submit():
        flash(u'登录成功！', category="success")
        return redirect(url_for('blog.index'))
    return render_template('blog.login.html', form=form)
