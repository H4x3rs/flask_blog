#! /env python
# _*_ coding:utf8 _*_
# @author:Haojie Ren
# @time:2017/9/2 0:46

from os import path
from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import flash
from flask import url_for
from flask import request
from flask import session
from flask import current_app
from flask import g,make_response
from sqlalchemy import func
from sqlalchemy import desc
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required
from flask_principal import Identity,AnonymousIdentity,identity_changed,current_app

from flaskblog.models import db
from flaskblog.models.users import Users
from flaskblog.models.posts import Posts
from flaskblog.models.tags import Tags
from flaskblog.models.comments import Comments
from flaskblog.models.posts_tags import posts_tags

from flaskblog.form import CommentForm
from flaskblog.form import LoginForm

from flaskblog.extensions import facebook

# 定义蓝图
admin_blueprint = Blueprint('admin',  __name__,
			 template_folder='templates',
			 static_folder='static',
			 url_prefix='/admin')


@admin_blueprint.route('/')
def admin():
    return render_template('admin.html')



