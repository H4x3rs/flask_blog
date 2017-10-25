#! /env python
# -*- coding:utf8 -*-
# @author:ren
# @date:2017/10/25.18:11

from . import db

# posts与tags的关联表
posts_tags = db.Table(
    'posts_tags',
    db.Column('post_id', db.String(50), db.ForeignKey('posts.id')),
    db.Column('tag_id', db.String(50), db.ForeignKey('tags.id')))
