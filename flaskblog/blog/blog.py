#! /env python
# _*_ coding:utf8 _*_
# @author:Haojie Ren
# @time:2017/9/2 0:46

from flask import Blueprint,render_template,redirect,request
from flask import flash,url_for,session,current_app,g
from flask_login import login_user,logout_user,current_user,login_required
from flask_principal import Identity,AnonymousIdentity,identity_changed,current_app
from sqlalchemy import func,desc
from flaskblog.models import db
from flaskblog.models import Users
from flaskblog.models import Posts
from flaskblog.models import Tags
from flaskblog.models import Comments
from flaskblog.models import posts_tags

from ..form import CommentForm,LoginForm
from ..extensions import facebook

from . import blog_blueprint

def sidebar_data():
    recent = db.session.query(Posts).order_by(Posts.create_at.desc()).limit(10).all()
    top_tags = db.session.query(Tags, func.count(posts_tags.c.post_id).label('total')).join(posts_tags).group_by(Tags).order_by(desc('total')).limit(10).all()
    return recent, top_tags

@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def index(page=1):
    """View function for index page"""
    posts = Posts.query.order_by(Posts.create_at.desc()).paginate(page, 10)
    recent, top_tags = sidebar_data()
    return render_template('blog.index.html',title=u'无名万物',posts=posts,recent=recent,top_tags=top_tags)

@blog_blueprint.route('/post/<string:post_id>', methods=('GET','POST'))
def post(post_id):
    """View function for post page"""
    form = CommentForm()
    # validate验证通过，增加一条评论
    if form.validate_on_submit():
        if not g.user.is_authenticated:
            flash(u'请先登录!')
        comment = Comments(comment=form.comment.data)
        comment.user_id = g.user.id
        comment.post_id = post_id
        g.db.session.add(comment)
        g.db.session.commit()

    post = db.session.query(Posts).join(Users).filter(Posts.id==post_id).first_or_404()
    tags = post.tags
    comments = db.session.query(Comments, Users).filter(Comments.post_id==post.id).order_by(desc(Comments.create_at)).all()
    recent, top_tags = sidebar_data()
    return render_template('blog.post.html',title='post',post=post,tags=tags,comments=comments,recent=recent,form=form,top_tags=top_tags)

@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    """View function for tag page"""
    tag = db.session.query(Tags).filter_by(name=tag_name).first_or_404()
    posts = tag.posts.order_by(Posts.create_at.desc()).all()
    recent, top_tags = sidebar_data() 

    return render_template('blog.tags.html',tag=tag,posts=posts,recent=recent,top_tags=top_tags)

@blog_blueprint.route('/user/<string:user_id>')
def user(user_id):
    """View function for user page"""
    user = db.session.query(Users).filter_by(id=user_id).first_or_404()
    posts = user.posts.order_by(Posts.create_at.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('blog.user.html',user=user,posts=posts,recent=recent,top_tags=top_tags)

# 登入
@blog_blueprint.route('/login', methods=['GET','POST'])
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

        login_user(user,remember)
        flash(u'登陆成功.',category='success')
        identity_changed.send(current_app._get_current_object(),identity=Identity(user.id))
        return redirect(url_for('blog.index'))
    else:
        login_form = LoginForm()
        next = request.args.get('next')
        return render_template('blog.login.html',form=login_form,next=next)

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
        return 'Access denied:reason=%s error=%s'%(request.args['error_reason'],request.args['error_description'])
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
        user = Users(nickname=facebook_username, password='', email=facebook_email)
        g.db.session.add(user)
        g.db.session.commit()

    flash('You have been logged in by Facebook.', category='success')
    return  redirect(url_for('blog.index'))

# 登出
@blog_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
	
    identity_changed.send(current_app._get_current_object(),identity=AnonymousIdentity())

    flash(u"注销成功！",category="success")
    return redirect(url_for('blog.index'))


@blog_blueprint.route('/register')
def register():
    return render_template('blog.register.html')

@blog_blueprint.route('/about')
def about():
    return render_template('blog.about.html')

@blog_blueprint.route('/gallery')
def gallery():
    return render_template('blog.gallery.html')



