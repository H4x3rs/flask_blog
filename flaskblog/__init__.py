#! /env python
# _*_ coding:utf8 _*_
# @author:Ren
# @time:2017/8/30 21:44

from flask import Flask
from flask import redirect
from flask import url_for

from flask_principal import identity_loaded,RoleNeed,UserNeed
from flask_login import current_user

from config import DevConfig

from models import db

# 扩展
from extensions import bcrypt
from extensions import login_manager
from extensions import bootstrap
from extensions import principal

# blog视图函数
from blog import blog
from admin import admin
from api import api

def create_app(object_name=DevConfig):
    app = Flask(__name__)
    # Get the config from object od Devconfig
    app.config.from_object(object_name)
    # Init db object 
    db.init_app(app)
    # Init flask_login
    login_manager.init_app(app)
    bootstrap.init_app(app)
    principal.init_app(app)
    # Init the bcrypt via app object      
    # bcrypt.init_app(app)
    # Register the Blueprint into app object
    app.register_blueprint(blog.blog_blueprint)
    app.register_blueprint(admin.admin_blueprint)
    app.register_blueprint(api.api_blueprint)
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
	"""Change the role via add the need object into Role
	   Need the access the app object
	"""
	identity.user = current_user
	
	# add the userneed to the identity user object
	if hasattr(current_user, 'id'):
	    identity.provides.add(UserNeed(current_user.id))
	# Add each role to the identity user objcet
	if hasattr(current_user, 'roles'):
	    for role in current_user.roles:
		identity.provides.add(RoleNeed(role.role))

    @app.route('/')
    def index():
        return redirect(url_for('blog.index'))
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
