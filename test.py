# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'

from db.dbmanager import OrmManager
db_manager = OrmManager()
print db_manager.insert_article(data={'title':'test', 'contents':'test1234', 'user_id':1})
