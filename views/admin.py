# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'


from plate_base import *
from db.dbmanager import OrmManager


@app.route('/admin')
def admin():
    start_index = request.args.get("start_index", 0)
    paging_size = request.args.get("paging_size", 30)
    keyword = request.args.get("keyword", None)

    db_manager = OrmManager()
    result = db_manager.select_articles(start_index=start_index,
                                        paging_size=paging_size,
                                        keyword=keyword)

    for i, r in enumerate(result):
        result[i].ctime = result[i].ctime.strftime("%Y/%m/%d %H:%M:%S")
        result[i].author = db_manager.select_member_by_id(result[i].user_id).name

    return render_template("admin.html", title="ADMIN", result=result)


@app.route('/admin/member')
def admin_member():
    start_index = request.args.get("start_index", 0)
    paging_size = request.args.get("paging_size", 30)
    keyword = request.args.get("keyword", None)

    db_manager = OrmManager()
    result = db_manager.select_member(start_index=start_index,
                                        paging_size=paging_size,
                                        keyword=keyword)
    return render_template("member.html", title="ADMIN", result=result)



@app.route('/admin/article')
def admin_article():
    start_index = request.args.get("start_index", 0)
    paging_size = request.args.get("paging_size", 30)
    keyword = request.args.get("keyword", None)

    db_manager = OrmManager()
    result = db_manager.select_articles(start_index=start_index,
                                        paging_size=paging_size,
                                        keyword=keyword)

    for i, r in enumerate(result):
        result[i].ctime = result[i].ctime.strftime("%Y/%m/%d %H:%M:%S")
        result[i].author = db_manager.select_member_by_id(result[i].user_id).name

    return render_template("article.html", title="ADMIN", result=result)



@app.route('/admin/reply')
def admin_reply():
    # TODO : implement
    return render_template("reply.html", title="ADMIN")


@app.route('/admin/logout')
def admin_logout():
    print("logtout")
    # TODO : implement
    return redirect("/admin/login")

@app.route('/admin/login')
def admin_login():
    from api.api_response_data import APIResponse

    user = request.form['user'] if 'user' in request.form else None
    password = request.form['password'] if 'password' in request.form else None



    if user and password:
        db_manager = OrmManager()
        member = db_manager.select_member_by_user(user)
        if member.password == password:
            r = APIResponse(code=200, data=None).json
            r.set_cookie('AUTH', value='values')
            return r
    else:
        return APIResponse(code=401, data=None).json

