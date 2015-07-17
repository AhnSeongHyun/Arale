# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'

from arale_base import *
from arale_base import _conf
from db.dbmanager import OrmManager
from .api_response_data import APIResponse

db_manager = OrmManager(host=_conf.database.host, port=_conf.database.port, user=_conf.database.user, password=_conf.database.password, db=_conf.database.db)

@app.route('/api/member/auth',  methods=[POST])
def auth():
    logger.debug(request)
    try:
        user = request.form['user'] if 'user' in request.form else None
        password = request.form['password'] if 'password' in request.form else None

        if user and password:

            member = db_manager.select_member_by_user(user)
            if member and member.password == password:
                return APIResponse(code=200, data=None).json
            else:
                return APIResponse(code=401, data=None).json
        else:
            return APIResponse(code=401, data=None).json
    except Exception as e:
        logger.exception(e)
        return APIResponse(code=500, data=None, msg=str(e)).json



@app.route('/api/member/<int:id>',  methods=[DELETE])
def delete_member(id):
    logger.debug(request)
    try:
        db_manager.delete_member(id)
        return APIResponse(code=200, data=None).json
    except Exception as e:
        logger.exception(e)
        return APIResponse(code=500, data=None, msg=str(e)).json


@app.route('/api/member',  methods=[POST])
def register_member():
    logger.debug(request)

    try:
        user = request.form['user'] if 'user' in request.form else None
        password = request.form['password'] if 'password' in request.form else None
        name = request.form['name'] if 'name' in request.form else None

        if user and password:
            member = db_manager.insert_member(user=user, password=password, name=name)
            if member:
                return APIResponse(code=200, data=None).json
        else:
            return APIResponse(code=401, data=None).json
    except Exception as e:
        logger.exception(e)
        return APIResponse(code=500, data=None, msg=str(e)).json
