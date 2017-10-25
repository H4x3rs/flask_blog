#! /env python
# _*_ coding:utf8 _*_
# @Haojie Ren

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_moment import Moment

bcrypt = Bcrypt()
login_manager = LoginManager()
moment = Moment()


login_manager.login_view = "blog.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    """Load the user's info"""
    from flaskblog.models.users import Users
    return Users.query.filter_by(id=user_id).first()

