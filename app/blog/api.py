#! /env python
# _*_ coding:utf8 _*_
# @author:Haojie Ren
# @time:2017/9/2 0:46

from ..models import db, Users, Posts, Tags, Comments, posts_tags
from ..form import *
from ..extensions import facebook, cache
from flask import Blueprint, render_template, redirect, request, flash, url_for, session, current_app, g, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_principal import Identity, AnonymousIdentity, identity_changed, current_app
from sqlalchemy import func, desc

api_blueprint = Blueprint('api', __name__, url_prefix='/api')


def sidebar_data():
    recent = db.session.query(Posts.title, Posts.id).order_by(Posts.create_at.desc()).limit(10).all()
    top_tags = db.session.query(Tags.name, func.count(Posts.id).label('total')).outerjoin(posts_tags).outerjoin(
        Posts).group_by(Tags.id).order_by(desc('total')).all()
    return recent, top_tags

@api_blueprint.route('/<int:page>')
# @cache.cached(timeout=60)
def index(page=1):
    """View function for index page"""
    try:
        posts = db.session.query(Posts, Users).order_by(
            desc(Posts.create_at)).paginate(page, 10)
        recent, top_tags = sidebar_data()
        return jsonify({'code':200,'message':'success','data':"posts"})
    except Exception as e:
        print(e)
    finally:
        db.session.remove()

