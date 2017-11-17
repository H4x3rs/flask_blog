#! /env python
# _*_ coding:utf8 _*_
# @author:Haojie Ren
# @time:2017/9/2 0:46

from uuid import uuid4
from os import path
from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import flash
from flask import url_for
from flask import request
from flask import session
from flask import current_app
from flask import g,make_response
from flask import jsonify

from qiniu import Auth,put_file

q = Auth('ZQGHGo7Z_a3K3dwhOAu7O9sANFLNyHc1PxYUG8B9','ZJkO6SyZw-yZ2iE6N0IC1REiOp9Mn2CYidC41nop')

# 定义蓝图
api_blueprint = Blueprint('api',  __name__,
			 template_folder='templates',
			 static_folder='static',
			 url_prefix='/api')


@api_blueprint.route('/')
def api():
    return jsonify({'code':200,'message':'Welcome to my api!'})

@api_blueprint.route('/qiniu_uptoken')
def uptoken():
    key = uuid4()
    bucket_name = 'image'
    uptoken = q.upload_token(bucket_name,key,3600)
    return jsonify({'code':200,'key':key,'uptoken':uptoken})
    
@api_blueprint.route('/qiniu_upload',methods=['POST'])
def upload(uptoken):
    f = request.files('file')
    uptoken = uptoken
    ret, resp = qn.put_file(uptoken,None,f)
    if ret != None:
        return jsonify({'cdoe':200,'message':'upload succes!','url':'http://on24sykai.bkt.clouddn.com/'+ret[key]})
    else:
        return jsonify({'code':500,'message':'Error'+resp.text_body})


@api_blueprint.route('/qiniu_call')
def callback():
    filename = request.get('fname')
    filesize = request.get('fsize')
    print filename,filesize


