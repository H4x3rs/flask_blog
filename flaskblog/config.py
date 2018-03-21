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
    # 七牛云配置
    QINIU_AK='ZQGHGo7Z_a3K3dwhOAu7O9sANFLNyHc1PxYUG8B9'
    QINIU_SK='ZJkO6SyZw-yZ2iE6N0IC1REiOp9Mn2CYidC41nop'
    QINIU_BUCKET='image'
    # SQLALCHEY数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ghost:vhadnRG3$a<aasdfjDF@47.91.230.186:3306/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

# 生产环境的配置类，继承自onfig基类
class ProConfig(Config):
    """
    Production config class.
    """

# 开发环境的配置类，继承自config基类
class DevConfig(Config):
    """Devlopment config class"""
    # open the debug
    DEBUG = True
