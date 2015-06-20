# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'

from board_base import *
from db.dbmanager import OrmManager
from .api_response_data import APIResponse

# TODO : implement



@app.route('/api/reply',  methods=[POST])
def write_reply():
    try:
        db_manager = OrmManager()
        reply_id = db_manager.insert_reply(request.form)
        return APIResponse(code=200, data={'reply_id': reply_id}).json

    except Exception as e:
        return APIResponse(code=500, data=None, msg=e).json


@app.route('/api/reply/<int:id>',  methods=[DELETE])
def delete_reply(id):
    try:
        db_manager = OrmManager()
        db_manager.delete_reply(id)
        return APIResponse(code=200, data=None).json
    except Exception as e:
        return APIResponse(code=500, data=None, msg=e).json


@app.route('/api/reply/<int:id>',  methods=[PUT])
def modify_reply(id):

    try:
        db_manager = OrmManager()
        result = db_manager.update_reply(id, request.form)
        return APIResponse(code=200, data=result.to_dict).json
    except Exception as e:
        return APIResponse(code=500, data=None, msg=e).json

@app.route('/api/reply/<int:id>',  methods=[GET])
def get_reply(id):

    try:
        db_manager = OrmManager()
        result = db_manager.select_reply_by_id(id)
        return APIResponse(code=200, data=result).json
    except Exception as e:
        return APIResponse(code=500, data=None, msg=e).json

@app.route('/api/reply',  methods=[GET])
def get_reply_by_article():

    try:
        article_id = request.args.get("article_id", None)
        if article_id:
            db_manager = OrmManager()
            result = db_manager.select_article_by_id(article_id)
            return APIResponse(code=200, data=result).json
        else:
            return APIResponse(code=400, data=None, msg='require article_id').json
    except Exception as e:
        return APIResponse(code=500, data=None, msg=e).json



