# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'

import traceback
from plate_base import *


@app.route('/test')
def test_index():
    try:
        from db.dbmanager import OrmManager
        from commons.paginator import Paginator


        db_manager = OrmManager()
        current_page = int(request.args.get('page', 1))
        paginator = Paginator(5)
        st_index, end_index, page_list= paginator.paging(current_page, db_manager.count())
        result = db_manager.select(st_index, paginator.page_per_count)
        return render_template('board_list.html', result=result, page_list=page_list, title=u'게시판')

    except Exception as e:
        print(e)
        print("Exception in user code:")
        print('-'*60)
        traceback.print_exc(file=sys.stdout)
        print('-'*60)


@app.route('/test/articles/new', methods=[GET])
def test_new_article():
    return render_template('board_writer.html', title=u'새글 쓰기')
