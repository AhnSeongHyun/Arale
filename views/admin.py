# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'


from board_base import *
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
    # TODO : implement
    return render_template("member.html", title="ADMIN")



@app.route('/admin/article')
def admin_article():
    # TODO : implement
    return render_template("article.html", title="ADMIN")



@app.route('/admin/reply')
def admin_reply():
    # TODO : implement
    return render_template("reply.html", title="ADMIN")
