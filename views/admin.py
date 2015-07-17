# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'
from arale_base import _conf
from arale_base import render_template
from arale_base import request
from arale_base import redirect, app, GET, POST, HEAD, PUT, DELETE
from arale_base import logging, logger
from arale_base import login_required, current_member, logout_member

from db.dbmanager import OrmManager
from functools import wraps

db_manager = OrmManager(host=_conf.database.host, port=_conf.database.port, user=_conf.database.user, password=_conf.database.password, db=_conf.database.db)


@app.route('/admin')
@login_required
def admin():

    logger.debug(str(request))
    start_index = request.args.get("start_index", 0)
    paging_size = request.args.get("paging_size", 30)
    keyword = request.args.get("keyword", None)


    result = db_manager.select_articles(start_index=start_index,
                                        paging_size=paging_size,
                                        keyword=keyword)

    for i, r in enumerate(result):
        result[i].ctime = result[i].ctime.strftime("%Y/%m/%d %H:%M:%S")
        result[i].author = db_manager.select_member_by_id(result[i].user_id).name

    return render_template("admin.html", result=result, member=current_member)


@app.route('/admin/member')
@login_required
def admin_member():
    logger.debug(request)
    start_index = request.args.get("start_index", 0)
    paging_size = request.args.get("paging_size", 30)
    keyword = request.args.get("keyword", None)

    result = db_manager.select_member(start_index=start_index,
                                        paging_size=paging_size,
                                        keyword=keyword)
    return render_template("member.html", result=result, member=current_member)



@app.route('/admin/article')
@login_required
def admin_article():

    start_index = request.args.get("start_index", 0)
    paging_size = request.args.get("paging_size", 30)
    keyword = request.args.get("keyword", None)

    result = db_manager.select_articles(start_index=start_index,
                                        paging_size=paging_size,
                                        keyword=keyword)

    for i, r in enumerate(result):
        result[i].ctime = result[i].ctime.strftime("%Y/%m/%d %H:%M:%S")
        result[i].author = db_manager.select_member_by_id(result[i].user_id).name

    return render_template("article.html", result=result, member=current_member)



@app.route('/admin/reply')
@login_required
def admin_reply():
    start_index = request.args.get("start_index", 0)
    paging_size = request.args.get("paging_size", 30)
    keyword = request.args.get("keyword", None)

    result = db_manager.select_reply(start_index=start_index,
                                     paging_size=paging_size,
                                     keyword=keyword)

    for i, r in enumerate(result):
        result[i].ctime = result[i].ctime.strftime("%Y/%m/%d %H:%M:%S")

    return render_template("reply.html", result=result, member=current_member)


@app.route('/admin/logout')
@login_required
def admin_logout():
    return logout_member()


@app.route('/admin/login', methods=[GET, POST])
def admin_login():
    if request.method == GET:
        return render_template("login.html")
    else:
        from api.api_response_data import APIResponse
        user = request.form['user'] if 'user' in request.form else None
        password = request.form['password'] if 'password' in request.form else None

        if user and password:
            member = db_manager.select_member_by_user(user)
            if member and member.password == password:
                response = APIResponse(code=200, data=None).json 
                from commons.aes256 import AESCipher
                import json
                aes = AESCipher(_conf.membership.key)
                response[0].set_cookie('AUTH', value=aes.encrypt(json.dumps(member.to_dict)))
                return response
            else:
                return APIResponse(code=401, data=None).json
        else:
            return APIResponse(code=400, data=None).json
