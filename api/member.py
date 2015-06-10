# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'

from board_base import *
from db.dbmanager import OrmManager
from api_response_data import APIResponse


@app.route('/api/member/auth',  methods=[POST])
def auth():
    user = request.form['user'] if 'user' in request.form else None
    password = request.form['password'] if 'password' in request.form else None

    if user and password:
        db_manager = OrmManager()
        member = db_manager.select_member(user)
        if member.password == password:
            return APIResponse(code=200, data=None).json
        else:
            return APIResponse(code=401, data=None).json

    else:
        return APIResponse(code=401, data=None).json
