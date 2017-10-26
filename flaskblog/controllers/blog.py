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
from sqlalchemy import func
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

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
blog_blueprint = Blueprint('blog',  __name__,
			 template_folder=path.join(path.pardir, 'templates', 'blog'), 
			 url_prefix='/blog')

def sidebar_data():
    recent = db.session.query(Posts).order_by(Posts.create_at.desc()).limit(5).all()
    top_tags = db.session.query(Tags, func.count(posts_tags.c.post_id).label('total')).join(posts_tags).group_by(
        Tags).order_by('total DESC').limit(10).all()
    return recent, top_tags

@blog_blueprint.route('/test')
def test():
    pages = Posts.query.order_by(Posts.create_at.desc()).paginate(1, 10)
    posts = pages.items
    recent, top_tags = sidebar_data()

    return render_template('index.html',
                           title=u'无名万物',
                           posts=posts,
                           pages=pages,
                           recent=recent,
                           top_tags=top_tags)


@blog_blueprint.route('/')
@blog_blueprint.route('/index')
@blog_blueprint.route('/<int:page>')
def index(page=1):
    """View function for index page"""
    pages = Posts.query.order_by(Posts.create_at.desc()).paginate(page, 10)
    posts = pages.items
    recent, top_tags = sidebar_data()

    return render_template('base.html',
                           title=u'无名万物',
                           posts=posts,
                           pages=pages,
                           recent=recent,
                           top_tags=top_tags)


@blog_blueprint.route('/post/<string:post_id>', methods=('GET','POST'))
def post(post_id):
    """View function for post page"""
    form = CommentForm()
    # validate验证通过，增加一条评论
    if form.validate_on_submit():
        comment = Comments(name=form.name.data, email=form.email.data, comment=form.comment.data)
        comment.post_id = post_id
        db.session.add(comment)
        db.session.commit()

    post = db.session.query(Posts).join(Users).filter(Posts.id==post_id).first_or_404()
    tags = post.tags
    comments = post.comments.order_by(Comments.create_at.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('post.html',
                           post=post,
                           tags=tags,
                           comments=comments,
                           recent=recent,
                           form=form,
                           top_tags=top_tags)


@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    """View function for tag page"""

    tag = db.session.query(Tags).filter_by(name=tag_name).first_or_404()
    posts = tag.posts.order_by(Posts.create_at.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('tags.html',
                           tag=tag,
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)


@blog_blueprint.route('/user/<string:id>')
def user(id):
    """View function for user page"""
    user = db.session.query(Users).filter_by(id=id).first_or_404()
    posts = user.posts.order_by(Posts.create_at.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('user.html',
                           user=user,
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)

# 登入
@blog_blueprint.route('/login', methods=('GET','POST'))
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = Users.query.filter_by(email=login_form.email.data).one()
        if not user:
            print "not user"
            flash(u"无效的用户名与密码！")

        login_user(user, login_form.remember.data)
        flash(u"登录成功!", category="success")
        return redirect(request.referrer or url_for('blog.index'))

    return render_template('login.html',
                           form=login_form)

# facebook 授权登陆
@blog_blueprint.route('/facebook')
def facebook_login():
    return facebook.authorize(callback=url_for('blog.facebook_authorized',
                                               next=request.referrer or None,
                                               _external=True))

@blog_blueprint.route('/facebook/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied:reason=%s error=%S'%(request.args['error_reason'],request.args['error_description'])
    session['facebook_oauth_token'] = (resp['access_token'],'')
    me = facebook.get('/me')
    if me.data.get('first_name', False):
        facebook_username = me.data['first_name']+" "+ me.data['last_name']
    else:
        facebook_username = me.data['name']
    if me.data.get('email', False):
        facebook_email = me.data['email']
    if me.data.get('phone', False):
        facebook_phone = me.data['phone']

    user = Users.query.filter_by(nickname=facebook_username).first()
    if user is None:
        user = Users(nickname=facebook_username, password='', email=facebook_email,phone=facebook_phone)
        db.session.add(user)
        db.session.commit()

    flash('You have been logged in by Facebook.', category='success')
    return  redirect(url_for('blog.index'))

# 登出
@blog_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u"注销成功！",category="success")
    return redirect(request.referrer or url_for('blog.index'))


@blog_blueprint.route('/register')
def register():
    return render_template('register.html')

@blog_blueprint.route('/about')
def about():
    return render_template('about.html')

@blog_blueprint.route('/gallery')
def gallery():
    return render_template('gallery.html')

@blog_blueprint.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@blog_blueprint.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500
