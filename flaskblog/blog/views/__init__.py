#! /env python
# -*- coding:utf8 -*-
# @author:ren
# @date:2018/3/22.10:57


from flask import Blueprint

blog_blueprint = Blueprint('blog', __name__, template_folder='templates', static_folder='static',
                           url_prefix='/blog')

__all__ = ['blog_blueprint']