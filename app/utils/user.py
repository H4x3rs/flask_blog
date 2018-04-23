#! /env python
# _*_ coding:utf8 _*_
# @author:Ren

import functools

from flask import g, request, session, current_app, flash, url_for, redirect, abort


class RequireRole(object):
    def __init__(self, role):
        self.role = role

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            if not g.user:
                url = url_for('account,login')
                if '?' not in url:
                    url += "?next=" + request.url
                return redirect(url)
            if self.role is None:
                return method(*args, **kwargs)
            if g.user.role == "new":
                flash(u'请先验证邮箱！', 'warn')
                # 验证邮箱
                return redirect(url_for('account.setting'))
            if g.user.role == 'admin':
                return redirect(url_for('admin.index'))
            return method(*args, **kwargs)

        return wrapper


require_login = RequireRole(None)
require_admin = RequireRole('admin')
