#! /env python
# _*_ coding:utf8 _*_
# @author:Ren
# @time:2017/8/30 21:44

from flask import Flask
from flask import redirect
from flask import url_for

from config import DevConfig

from models import db

# 扩展
from extensions import bcrypt
from extensions import login_manager
from extensions import bootstrap

# blog视图函数
from controllers import blog

def create_app(object_name=DevConfig):
    app = Flask(__name__)
    # Get the config from object od Devconfig
    app.config.from_object(object_name)
    # Init db object 
    db.init_app(app)
    # Init flask_login
    login_manager.init_app(app)
    bootstrap.init_app(app)
    # Init the bcrypt via app object      
    # bcrypt.init_app(app)
    # Register the Blueprint into app object
    app.register_blueprint(blog.blog_blueprint)
	
    @app.route('/')
    def index():
        return redirect(url_for('blog.index'))
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
