#! /env python
# _*_ coding:utf8 _*_
# @Haojie Ren

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_moment import Moment
from flask_oauthlib.client import OAuth
from flask_principal import Principal,Permission,RoleNeed

bcrypt = Bcrypt()
login_manager = LoginManager()
moment = Moment()
oauth = OAuth()
principal = Principal()

login_manager.login_view = "blog.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"

facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/facebook/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key='1445736152161924',
                            consumer_secret='3813037e74636c105e19669930957972',
                            request_token_params={'scope':'email'})

@login_manager.user_loader
def load_user(user_id):
    """Load the user's info"""
    from flaskblog.models.users import Users
    return Users.query.filter_by(id=user_id).first()

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_oauth_token')

# Init the role permission via RoleNeed(Need)
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))
