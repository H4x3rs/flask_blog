#! /env python
# _*_ coding:utf8 _*_
# @author:Ren
# @time:2017/8/30 22:06

# 配置的基类
class Config(object):
    """
    Base config class.
    """
    HOST = '0.0.0.0'
    PORT = 5000
    CSRF_ENABLED = True
    SECRET_KEY = '0839a4faf06c5a0dfb442226e4887ce4'

# 生产环境的配置类，继承自onfig基类
class ProConfig(Config):
    """
    Production config class.
    """
    pass

# 开发环境的配置类，继承自config基类
class DevConfig(Config):
    """
    Devlopment config class
    """
    # open the debug
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ghost:vhadnRG3$a<aasdfjDF@localhost:3306/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
