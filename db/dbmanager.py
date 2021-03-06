# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'


import datetime
from arale_base import logger
from sqlalchemy import create_engine, desc
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from .mapper import Article, Reply, Member

class OrmManager(object):

    session = None
    connection_string = None

    host = None
    user = None
    pasword = None
    db = None
    port = 3306


    def __init__(self, host=None, port=3306, user=None, password=None, db=None):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port

        self.connection_string = 'mysql+pymysql://'+self.user +':'+self.password + '@' + self.host+':'+str(self.port)+'/' +self.db

    def open(self):
        try:
            engine = create_engine(self.connection_string)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        except Exception as e:
            logger.exception(e)
            raise e

    def insert_or_update_article(self, data):
        try:
            self.open()
            article = Article(title=data['title'],
                              contents=data['contents'],
                              ctime=datetime.datetime.now(),
                              mtime=None,
                              user_id=data['user_id'])

            is_new_article = True
            if 'id' in data:
                exist_article = self.session.query(Article).filter(Article.id == data['user_id']).scalar()
                if exist_article:  # modify
                    is_new_article = False

            if is_new_article:
                self.session.add(article)

            else:

                exist_article.title = article.title
                exist_article.contents = article.contents
                exist_article.ctime = article.ctime
                exist_article.mtime = article.mtime
                exist_article.user_id = article.user_id

            self.session.commit()
            self.session.refresh(article)
            self.session.close()
            return article.id
        except Exception as e:
            logger.exception(e)
            self.close()
            raise e

    def update_article(self, id, data):
        try:
            self.open()
            article = self.session.query(Article).filter(Article.id == id).one()

            if 'title' in data:
                article.title = data['title']

            if 'contents' in data:
                article.contents = data['contents']

            article.mtime = datetime.datetime.now()
            self.session.commit()
            result = self.session.query(Article).filter(Article.id == id).one()
            self.close()
            return result
        except Exception as e:
            logger.exception(e)
            self.close()
            raise e

    def delete_article(self, id):
        try:
            self.open()
            article = self.session.query(Article).filter(Article.id == id).one()
            self.session.delete(article)
            self.session.commit()
            self.session.close()

        except Exception as e:
            logger.exception(e)
            self.close()
            raise e

    def select_article_by_id(self, id):
        try:
            self.open()
            article = self.session.query(Article).filter(Article.id == id).one()
            self.close()
            return article
        except Exception as e:
            logger.exception(e)
            self.close()
            raise e

    def select_articles(self, start_index=0, paging_size=30, keyword=None):
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
            logger.exception(e)
            self.close()
            raise e

    def count_article(self):
        try:
            self.open()
            total_count = self.session.query(func.count(Article.id)).scalar()
            return total_count
        except Exception as e:
            logger.exception(e)
            self.close()
            raise e

    def insert_reply(self, data):
        try:
            self.open()
            reply = Reply(article_id=data['article_id'],
                          contents=data['contents'],
                          ctime=datetime.datetime.now(),
                          mtime=None,
                          parent_reply_id=None)

            self.session.add(reply)
            self.session.commit()
            self.session.refresh(reply)
            self.session.close()
            return reply.id
        except Exception as e:
            logger.exception(e)
            self.close()
            raise e

    def update_reply(self, id, data):
        try:
            self.open()
            article = self.session.query(Reply).filter(Reply.id == id).one()
            article.contents = data['contents']
            article.mtime = datetime.datetime.now()
            self.session.commit()
            result = self.session.query(Reply).filter(Reply.id == id).one()
            self.close()
            return result
        except Exception as e:
            logger.exception(e)
            self.close()
            raise e

    def delete_reply(self, id):
        try:
            self.open()
            reply = self.session.query(Reply).filter(Reply.id == id).one()
            self.session.delete(reply)
            self.session.commit()
            self.session.close()

        except Exception as e:
            logger.exception(e)
            self.close()
            raise e

    def select_reply(self, start_index=0, paging_size=30, keyword=None):
        try:
            self.open()
            q = self.session.query(Reply)
            if keyword:
                q = q.filter(or_(Reply.contents.like("%" + keyword + "%")))

            q = q.order_by(desc(Reply.ctime))
            q = q.offset(start_index)
            q = q.limit(paging_size)
            result = q.all()
            self.close()
            return result
        except Exception as e:
            logger.exception(e)
            self.close()
            raise e


    def select_reply_by_id(self, id):
        try:
            self.open()
            reply = self.session.query(Reply).filter(Reply.id == id).scalar()
            self.close()
            return reply
        except Exception as e:
            logger.exception(e)
            self.close()
            raise e


    def select_reply_by_article(self, article_id):
        try:
            self.open()
            replies = self.session.query(Reply).filter(Reply.article_id == article_id).all()
            self.close()
            return replies
        except Exception as e:
            logger.exception(e)
            self.close()
            raise e

    def count_reply_by_article(self, article_id):
        try:
            self.open()
            total_count = self.session.query(func.count(Reply.id)).filter(Reply.article_id == article_id).scalar()
            return total_count
        except Exception as e:
            logger.exception(e)
            self.close()
            raise e

    def insert_member(self, user, password, name=None):
        try:
            self.open()
            member = Member(user, password, name)
            self.session.add(member)
            self.session.commit()
            self.session.refresh(member)
            self.session.close()
            return member.id
        except Exception as e:
            logger.exception(e)
            self.close()
            raise e


    def select_member(self, start_index=0, paging_size=30, keyword=None):
        try:
            self.open()
            q = self.session.query(Member)
            if keyword:
                q = q.filter(or_(Member.name.like("%" + keyword + "%"), Member.user.like("%" + keyword + "%")))

            q = q.offset(start_index)
            q = q.limit(paging_size)
            result = q.all()
            self.close()
            return result
        except Exception as e:
            logger.exception(e)
            self.close()
            raise e


    def select_member_by_user(self, user):
        try:
            self.open()
            member = self.session.query(Member).filter(Member.user == user).scalar()
            self.close()
            return member
        except Exception as e:
            logger.exception(e)
            self.close()
            raise e

    def select_member_by_id(self, user_id):

        try:
            self.open()
            member = self.session.query(Member).filter(Member.id == user_id).scalar()
            self.close()
            return member
        except Exception as e:
            logger.exception(e)
            self.close()
            raise e

    def delete_member(self, user_id):
        try:
            self.open()
            member = self.session.query(Member).filter(Member.id == user_id).scalar()
            self.session.delete(member)
            self.session.commit()
            self.session.close()

        except Exception as e:
            logger.exception(e)
            self.close()
            raise e

    def close(self):
        if self.session:
            self.session.close()
