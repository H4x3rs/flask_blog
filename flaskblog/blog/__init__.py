#! /env python
# -*- coding:utf8 -*-
# @author:ren
# @date:2018/3/22.10:57


from .account import account_blueprint
from .blog import blog_blueprint

__all__ = ['blog_blueprint', 'account_blueprint']
