#! /env python
# -*- coding:utf8 -*-
# @author:ren
# @date:2018/4/12.16:56

from flask import Blueprint, request, jsonify, current_app, url_for,render_template,send_file
from PIL import Image
from uuid import uuid4
import datetime
import os

upload_blueprint = Blueprint('upload', __name__, static_folder='upload', url_prefix='/upload')


@upload_blueprint.route('/', methods=['POST'])
def upload():
    if "image" not in request.files:
        current_app.logger.error('not file part')
        return jsonify({'code': -1, 'message': "not file part"})
    file = request.files['image']
    if file:
        filename = str(datetime.date.year)+"/"+str(datetime.date.month)+"/"+str(uuid4())
        file.save(os.path.join(upload_blueprint.static_folder,filename))
        file_url = url_for('upload.static',filename,_external=True)
        return jsonify({'code': 200, 'msg': "上传成功",'file_path':file_url,'success':'true'})


@upload_blueprint.route('/<filename>')
def upload_file(filename):
    return jsonify(
        {'code': 200, "message": "success", 'filename': filename, 'pic': url_for('upload.static', filename=filename, _external=True)})
