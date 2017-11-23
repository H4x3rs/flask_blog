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

from flaskblog.form import PostForm

from flaskblog.extensions import facebook

# 定义蓝图
admin_blueprint = Blueprint('admin',  __name__,
			 template_folder='templates',
			 static_folder='static',
			 url_prefix='/admin')


@admin_blueprint.route('/')
def admin():
    return render_template('admin.html')

@admin_blueprint.route('/list_blog',methods=['GET','DELETE'])
@login_required
def list_blog(id=None):
    if request.method == 'DELETE':
	post = db.session.query(Posts).filter_by(id=id,user_id=current_user.id).first_or_404()
	db.session.delete(post)
	db.session.commit()
    user_blog = db.session.query(Posts).filter_by(user_id=current_user.id).all()
    return render_template('list_blog.html',user_blog=user_blog)

@admin_blueprint.route('/edit_blog/<string:id>')
@login_required
def edit_blog(id):
    blog = db.session.query(Posts).filter_by(id=id).first_or_404()
    
    return render_template('edit_blog.html',blog=blog) 

@admin_blueprint.route('/new_blog',methods=['GET','POST'])
@login_required
def new_blog():
    form = PostForm()
    if request.method == 'GET':
	return render_template('new_blog.html')

    if request.method == 'POST':
	if form.validate_on_submit():
	    post = Post(title=form.title.data, post=form.post.data)
	    post.user_id = current_user.id
	    db.session.add(post)
	    db.session.commit()
	    return render_template('list_blog.html')


