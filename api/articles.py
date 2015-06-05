# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'

from board_base import *
from db.dbmanager import OrmManager
import traceback
from api_response_data import APIResponse

@app.route('/api/articles',  methods=[GET])
def get_article_list():
    db_manager = OrmManager()


@app.route('/api/articles',  methods=[POST])
def write_article():
    try:
        db_manager = OrmManager()
        db_manager.insert_new(request.form)
        return APIResponse(code=200, data=None).json

    except Exception as e:
        return APIResponse(code=500, data=None, msg=e).json


@app.route('/api/articles/<int:id>',  methods=[DELETE])
def delete_article(id):
    db_manager = OrmManager()
    try:
        db_manager.delete(id)
        return APIResponse(code=200, data=None).json
    except Exception as e:
        return APIResponse(code=500, data=None, msg=e).json


@app.route('/api/articles/<int:id>',  methods=[PUT])
def modify_article(id):
    db_manager = OrmManager()
    try:
        result = db_manager.update(id, request.form)
        return APIResponse(code=200, data=result).json
    except Exception as e:
        return APIResponse(code=500, data=None, msg=e).json


@app.route('/api/articles/<int:id>',  methods=[GET])
def get_article(id):
    db_manager = OrmManager()
    try:
        result = db_manager.select_by_id(id)
        return APIResponse(code=200, data=result).json
    except Exception as e:
        return APIResponse(code=500, data=None, msg=e).json



