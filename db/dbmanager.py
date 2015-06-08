# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'


import datetime
from sqlalchemy import create_engine, desc
from sqlalchemy import func 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from mapper import *

CONNECTION_STRING = 'sqlite:///db/db.sqlite'


class OrmManager(object):

    session = None  

    def open(self):
        try:
            engine = create_engine(CONNECTION_STRING)
            Session = sessionmaker(bind=engine) 
            self.session = Session()
        except Exception as e:
            raise e

    def insert_article(self, data):

        try:

            self.open()

            article = Article(title=data['title'], contents=data['contents'], ctime=datetime.datetime.now(), mtime=None)

            self.session.add(article)
            self.session.commit()
            self.session.refresh(article)
            self.session.close()
            return article.id
        except Exception as e:
            self.close()
            raise e

    def update_article(self, id, data):
        try:
            self.open()
            article = self.session.query(Article).filter(Article.id==id).one()

            article.title = data['title']
            article.contents = data['contents']
            article.mtime = datetime.datetime.now()
            self.session.commit()
            result = self.session.query(Article).filter(Article.id==id).one()
            self.close()
            return result
        except Exception as e:
            self.close()
            raise e

    def delete_article(self, id):
        try:
            self.open()
            article = self.session.query(Article).filter(Article.id==id).one()
            self.session.delete(article)
            self.session.commit()
            self.session.close()

        except Exception as e:
            self.close()
            raise e

    def select_article_by_id(self, id):
        try:
            self.open()
            article = self.session.query(Article).filter(Article.id==id).one()
            self.close()
            return article
        except Exception as e:
            self.close()
            raise e

    def select_articles(self, start_index, paging_size, keyword=None):
        try:
            self.open()
            q = self.session.query(Article)
            if keyword:
                q = q.filter(or_(Article.title.like("%" + keyword + "%"), Article.contents.like("%" + keyword + "%")))

            q = q.order_by(desc(Article.ctime))
            q = q.offset(start_index)
            q = q.limit(paging_size)
            result = q.all()
            self.close()
            return result
        except Exception as e:
            self.close()
            raise e

    def count_article(self):
        try:
            self.open()
            total_count = self.session.query(func.count(Article.id)).scalar()
            return total_count
        except Exception as e:
            self.close()
            raise e  

    def close(self):
        if self.session:
                self.session.close()
