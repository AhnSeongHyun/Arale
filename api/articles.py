# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'

from arale_base import *
from db.dbmanager import OrmManager
from .api_response_data import APIResponse


@app.route('/api/articles',  methods=[GET])
def get_article_list():
    logger.debug(request)

    try:
        start_index = request.args.get("start_index", 0)
        paging_size = request.args.get("paging_size", 30)
        keyword = request.args.get("keyword", None)

        db_manager = OrmManager()
        articles = db_manager.select_articles(start_index=start_index,
                                            paging_size=paging_size,
                                            keyword=keyword)

        result = [a.to_dict for a in articles]
        return APIResponse(code=200, data=result).json
    except Exception as e:
        logger.exception(e)
        return APIResponse(code=500, data=None, msg=str(e)).json



@app.route('/api/articles',  methods=[POST])
def write_article():
    logger.debug(request)
    try:
        db_manager = OrmManager()
        article_id = db_manager.insert_or_update_article(request.form.to_dict())
        return APIResponse(code=200, data={'article_id': article_id}).json
    except Exception as e:
        logger.exception(e)
        return APIResponse(code=500, data=None, msg=str(e)).json


@app.route('/api/articles/<int:id>',  methods=[DELETE])
def delete_article(id):
    logger.debug(request)
    try:
        db_manager = OrmManager()
        db_manager.delete_article(id)
        return APIResponse(code=200, data=None).json
    except Exception as e:
        logger.exception(e)
        return APIResponse(code=500, data=None, msg=str(e)).json


@app.route('/api/articles/<int:id>',  methods=[PUT])
def modify_article(id):
    logger.debug(request)
    try:
        db_manager = OrmManager()
        result = db_manager.update_article(id, request.form.to_dict())
        return APIResponse(code=200, data=result.to_dict).json
    except Exception as e:
        logger.exception(e)
        return APIResponse(code=500, data=None, msg=str(e)).json


@app.route('/api/articles/<int:id>',  methods=[GET])
def get_article(id):
    logger.debug(request)
    try:
        db_manager = OrmManager()
        result = db_manager.select_article_by_id(id)

        return APIResponse(code=200, data=result.to_dict).json
    except Exception as e:
        logger.exception(e)
        return APIResponse(code=500, data=None, msg=str(e)).json