#! /env python
# _*_ coding:utf8 _*_
# @author:Ren
# @time:2017/8/30 21:44

import jinja2
from flask import Flask
from flask import redirect
from flask import url_for
from flask_principal import identity_loaded,RoleNeed,UserNeed
from flask_login import current_user

from config import DevConfig
from config import Config
from config import ProConfig

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

# 默认情况下 Flask的jinja_loader将会从全局加载template，这将会导致多个蓝图
# 模板命名的冲突，导致加载模板出现混乱，该类继承Flask，通过将Flask自身的
# jinja_loader重写成一个ChoicLoader来选择jinja_loader，如果注册了蓝图，该
# 类实例将首先从蓝图目录加载template而不是全局，所以不会出现命名混乱的情况
# 但这将会导致调用模板必须添加蓝图前缀，但谁说这不是我的本意呢？
class App(Flask):
    """
    In general jinja_loader will load the template from global path
    If registered the blueprint
    jinja_loader will load the templates from the blueprint's path
    """
    def __init__(self):
        Flask.__init__(self,__name__)
        self.jinja_loader = jinja2.ChoiceLoader([self.jinja_loader,jinja2.PrefixLoader({},delimiter=".")])
    def create_global_jinja_loader(self):
        return self.jinja_loader
    def register_blueprint(self,bp):
        Flask.register_blueprint(self,bp)
        self.jinja_loader.loaders[1].mapping[bp.name] = bp.jinja_loader

# 创建App实例
def create_app(object_name=DevConfig):
    app = App()
    # Get the config from object od Devconfig
    app.config.from_object(object_name)
    # Init db object 
    db.init_app(app)
    # Init flask_login
    login_manager.init_app(app)
    principal.init_app(app)
    # Init the bcrypt via app object      
    # bcrypt.init_app(app)

    # Register the blog Blueprint into app object
    app.register_blueprint(blog.blog_blueprint)
    # Register the admin Blueprint into app object
    app.register_blueprint(admin.admin_blueprint)
    # Register the api Blueprint into app object
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
    app.run(host='0.0.0.0',port=5000)
