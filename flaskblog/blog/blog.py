#! /env python
# _*_ coding:utf8 _*_
# @author:Haojie Ren
# @time:2017/9/2 0:46

from ..models import db, Users, Posts, Tags, Comments, posts_tags
from ..form import *
from ..extensions import facebook, cache
from flask import Blueprint, render_template, redirect, request, flash, url_for, session, current_app, g
from flask_login import login_user, logout_user, current_user, login_required
from flask_principal import Identity, AnonymousIdentity, identity_changed, current_app
from sqlalchemy import func, desc

blog_blueprint = Blueprint('blog', __name__, template_folder='templates/blog', static_folder='static', url_prefix='/blog')


def sidebar_data():
    recent = db.session.query(Posts.title, Posts.id).order_by(Posts.create_at.desc()).limit(10).all()
    top_tags = db.session.query(Tags.name, func.count(Posts.id).label('total')).outerjoin(posts_tags).outerjoin(
        Posts).group_by(Tags.id).order_by(desc('total')).all()
    return recent, top_tags


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
# @cache.cached(timeout=60)
def index(page=1):
    """View function for index page"""
    try:
        posts = db.session.query(Posts, Users).filter(Posts.user_id == Users.id).order_by(
            desc(Posts.create_at)).paginate(page, 10)
        recent, top_tags = sidebar_data()
        return render_template('blog.index.html', title=u'无名万物', posts=posts, recent=recent, top_tags=top_tags)
    except Exception as e:
        print(e)
    finally:
        db.session.remove()


@blog_blueprint.route('/post/<string:post_id>', methods=('GET', 'POST'))
def post(post_id):
    """View function for post page"""
    form = CommentForm()
    # validate验证通过，增加一条评论
    if form.validate_on_submit():
        if g.user.is_authenticated:
            comment = Comments(comment=form.comment.data)
            comment.user_id = g.user.id
            comment.post_id = post_id
            g.db.session.add(comment)
            g.db.session.commit()
        else:
            flash(u'请先登录!')

    post = db.session.query(Posts, Users).filter(Posts.id == post_id).first_or_404()
    tags = post.Posts.tags
    comments = db.session.query(Comments, Users).filter(Comments.post_id == post.Posts.id).order_by(
        desc(Comments.create_at)).all()
    recent, top_tags = sidebar_data()
    return render_template('blog.post.html', title='post', post=post, tags=tags, comments=comments, recent=recent,
                           form=form, top_tags=top_tags)


@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    """View function for tag page"""
    page = request.args.get("page") or 1
    tags = db.session.query(Tags).filter_by(name=tag_name).first_or_404()
    tag_posts = db.session.query(Posts,Users.nickname, Tags).outerjoin(posts_tags).outerjoin(Tags).group_by(
        Posts.id).filter(Users.id == Posts.user_id).order_by(desc(Posts.create_at)).paginate(page,10)
    # posts = tags.posts.order_by(Posts.create_at.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('blog.tags.html', tag=tags, posts=tag_posts, recent=recent, top_tags=top_tags)


@blog_blueprint.route('/user/<string:user_id>')
def user(user_id):
    """View function for user page"""
    user = db.session.query(Users).filter_by(id=user_id).first_or_404()
    posts = user.posts.order_by(Posts.create_at.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('blog.user.html', user=user, posts=posts, recent=recent, top_tags=top_tags)


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
        return 'Access denied:reason=%s error=%s' % (request.args['error_reason'], request.args['error_description'])
    session['facebook_oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    if me.data.get('first_name', False):
        facebook_username = me.data['first_name'] + " " + me.data['last_name']
    else:
        facebook_username = me.data['name']
    if me.data.get('email', False):
        facebook_email = me.data['email']
    if me.data.get('phone', False):
        facebook_phone = me.data['phone']

    user = Users.query.filter_by(nickname=facebook_username).first()
    if user is None:
        user = Users(nickname=facebook_username, password='', email=facebook_email)
        g.db.session.add(user)
        g.db.session.commit()

    flash('You have been logged in by Facebook.', category='success')
    return redirect(url_for('blog.index'))


# # 登出
# @blog_blueprint.route('/logout')
# @login_required
# def logout():
#     logout_user()
#
#     identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
#
#     flash(u"注销成功！", category="success")
#     return render_template('blog.login.html')


# @blog_blueprint.route('/register')
# def register():
#     return render_template('blog.register.html')


@blog_blueprint.route('/about')
def about():
    return render_template('blog.about.html')


@blog_blueprint.route('/gallery')
def gallery():
    return render_template('blog.gallery.html')

@blog_blueprint.teardown_request
def shutdown_session(exception=None):
    try:
        db.session.remove()
    except Exception as e:
        print(e)