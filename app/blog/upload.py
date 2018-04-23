#! /env python
# _*_ coding:utf8 _*_
# @author:Ren
# @time:2018/4/15 23:38


from flask import Blueprint, request, jsonify, current_app, url_for
from PIL import Image, ImageDraw
from uuid import uuid4
from datetime import datetime
import os
import imghdr
import filetype

upload_blueprint = Blueprint('upload', __name__, static_folder='image', url_prefix='/upload')

allow_type = ['png','gif','jpeg']

@upload_blueprint.route('/', methods=['GET', 'POST'])
def upload():
    file = request.files['image']
    file_type = imghdr.what(file)
    print(file_type)
    if file_type not in allow_type:
        return jsonify({'code': 400, 'msg': '图片格式不正确！', 'success': 'false'})
    if file:
        # 存储路径
        path = os.path.join(upload_blueprint.static_folder)
        # 按年月分目录
        year, month = (str(datetime.now().year), str(datetime.now().month))
        # uuid生成文件名
        name = str(uuid4()).replace("-", "") + ".jpg"
        # 判断目录是否存在
        if not os.path.exists(os.path.join(path, year, month)):
            current_app.logger.debug("该目录不存在：{}".format(os.path.join(path, year, month)))
            current_app.logger.info("即将创建该目录：{}".format(os.path.join(path, year, month)))
            os.makedirs(os.path.join(path, year, month), 755)
            current_app.logger.info("目录创建完成：{}".format(os.path.join(path, year, month)))
        file.save(os.path.join(path, year, month, name))
        current_app.logger.info("文件上传完成：{}".format(name))
        file_url = url_for('upload.static', filename="{}/{}/{}".format(year,month,name), _external=True)
        print(file_url)
        return jsonify({'code': 200, 'msg': '上传成功', 'file_path': file_url, 'success': 'true'})


@upload_blueprint.route('/<string:year>/<string:month>/<string:name>')
def upload_file(year, month, name):
    print(os.path.exists(os.path.join(upload_blueprint.static_folder, year, month, name)))
    if os.path.exists(os.path.join(upload_blueprint.static_folder, year, month, name)):
        return jsonify({'code': 200, "message": "success", 'filename': name,
                        'pic': url_for('upload.static', filename=os.path.join(year, month, name), _external=True)})
