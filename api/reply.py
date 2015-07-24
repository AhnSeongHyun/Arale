# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'

from arale_base import *
from arale_base import _conf
from db.dbmanager import OrmManager
from .api_response_data import APIResponse

db_manager = OrmManager(host=_conf.database.host,
                        port=_conf.database.port,
                        user=_conf.database.user,
                        password=_conf.database.password,
                        db=_conf.database.db)

@app.route('/api/reply',  methods=[POST])
def write_reply():
    logger.debug(request)
    try:
        reply_id = db_manager.insert_reply(request.form)
        return APIResponse(code=200, data={'reply_id': reply_id}).json
    except Exception as e:
        logger.exception(e)
        return APIResponse(code=500, data=None, msg=e).json


@app.route('/api/reply/<int:id>',  methods=[DELETE])
def delete_reply(id):
    logger.debug(request)
    try:
        db_manager.delete_reply(id)
        return APIResponse(code=200, data=None).json
    except Exception as e:
        logger.exception(e)
        return APIResponse(code=500, data=None, msg=e).json


@app.route('/api/reply/<int:id>',  methods=[PUT])
def modify_reply(id):
    logger.debug(request)
    try:
        result = db_manager.update_reply(id, request.form)
        return APIResponse(code=200, data=result.to_dict).json
    except Exception as e:
        logger.exception(e)
        return APIResponse(code=500, data=None, msg=e).json

@app.route('/api/reply/<int:id>',  methods=[GET])
def get_reply(id):
    logger.debug(request)
    try:
        result = db_manager.select_reply_by_id(id)
        return APIResponse(code=200, data=result.to_dict).json
    except Exception as e:
        logger.exception(e)
        return APIResponse(code=500, data=None, msg=e).json

@app.route('/api/reply',  methods=[GET])
def get_reply_by_article():
    logger.debug(request)
    try:
        article_id = request.args.get("article_id", None)
        if article_id:
            replies = db_manager.select_reply_by_article(article_id)
            result = [r.to_dict for r in replies]
            return APIResponse(code=200, data=result).json
        else:
            return APIResponse(code=400, data=None, msg='require article_id').json
    except Exception as e:
        logger.exception(e)
        return APIResponse(code=500, data=None, msg=e).json
