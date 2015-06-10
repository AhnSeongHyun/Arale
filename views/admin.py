# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'


from board_base import *


@app.route('/admin')
def index():
    return render_template("admin.html")
