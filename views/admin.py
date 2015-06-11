# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'


from board_base import *


@app.route('/admin')
def admin():
    # TODO : implement
    return render_template("admin.html", title="ADMIN")


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
