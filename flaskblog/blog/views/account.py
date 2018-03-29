#! /env python
# _*_ coding:utf8 _*_
# @author:Ren

from flask import current_app, redirect, flash, url_for, request, render_template
from flask_login import login_required, logout_user,login_user
from flask_principal import identity_changed, AnonymousIdentity,Identity

from .. import blog_blueprint
from ...form import LoginForm
from ...models import Users


@blog_blueprint("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        next = request.form.get('next')
        remember = request.form.get('remember')

        user = Users.query.filter_by(email=email).one()
        if not user:
            flash(u'无效的用户名!')
        if not user.check_password(password):
            flash(u'无效的密码!')

        login_user(user, remember)
        flash(u'登陆成功.', category='success')
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
        return redirect(url_for('blog.index'))
    else:
        login_form = LoginForm()
        next = request.args.get('next')
        return render_template('blog.login.html', form=login_form, next=next)


# 登出
@blog_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    flash(u"注销成功！", category="success")

    return redirect(url_for('blog.index'))


# 注册
@blog_blueprint.route('/register', methods=['GET','POST'])
def register():
    return render_template('blog.register.html')