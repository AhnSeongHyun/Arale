# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'

import sys
reload(sys)
sys.setdefaultencoding('ms949')

from board_base import *

import api
import views

if __name__ == "__main__":
    app.run()


# @app.route('/articles',  methods=[GET, POST])
# def articles():
#     result = None
#     try:
#         if request.method == POST:
#             if is_ajax(request):
#                 __g_orm.insert_reply(request.form)
#             else:
#                 __g_orm.insert_new(request.form)
#
#         if is_ajax(request):
#             return jsonify(), 200
#         else:
#             current_page = int(request.args.get('page', 1))
#
#             pgn = Paginator(5)
#             st_index, end_index, page_list= pgn.paging(current_page, __g_orm.count())
#             result = __g_orm.select(st_index, pgn.page_per_count)
#
#             return render_template('board_list.html', result=result, page_list=page_list, title=u'게시판')
#
#     except Exception as e:
#         print("Exception in user code:")
#         print('-'*60)
#         traceback.print_exc(file=sys.stdout)
#         print('-'*60)



# def is_ajax(request):
#     return request.is_xhr
#
#
#
# @app.route('/articles/update/<id>', methods=[GET])
# def update_article(id):
#     result = None
#     try:
#         result = __g_orm.select_by_id(id)
#     except Exception as e:
#         print(e)
#     return render_template('board_update.html', result=result, title=u'수정하기')
#
#
# @app.route('/articles/reply/<id>', methods=[GET])
# def reply_article(id):
#     result = None
#     try:
#         result = __g_orm.select_by_id(id)
#     except Exception as e:
#         print(e)
#
#     return render_template('board_reply.html', result=result, title=u'답글달기')
#
#
# @app.route('/articles/<id>', methods=[GET, DELETE, PUT])
# def article(id):
#     if request.method == GET:
#         result = None
#         try:
#             result = __g_orm.select_by_id(id)
#         except Exception as e:
#             print(e)
#
#         return render_template('board_view.html', result=result, title=u'글 보기')
#
#     elif request.method == PUT:
#         try:
#             result = __g_orm.update(id, request.form)
#         except Exception as e:
#             print(e)
#             return jsonify({"id":id}), 500
#
#         return jsonify({"id":id}), 200
#
#     elif request.method == 'DELETE':
#         response = None
#         try:
#             response = jsonify({"id":id})
#             __g_orm.delete(id)
#             return jsonify({"id":id}), 200
#
#         except Exception as e:
#             print(e)
#             return jsonify({"id":id}), 500
#
#
    
