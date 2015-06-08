# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text

import datetime
Base = declarative_base()


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    contents = Column(Text, nullable=True)
    ctime = Column(DateTime, nullable=False)
    mtime = Column(DateTime, nullable=True)

    def __init__(self, title, contents, ctime, mtime):
        self.title = title
        self.contents = contents
        self.ctime = ctime 
        self.mtime = mtime

    def __str__(self):
        return str(self.__dict__)

class Reply(Base):
    __tablename__ = 'reply'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, nullable=False)
    contents = Column(Text, nullable=True)
    ctime = Column(DateTime, nullable=False)
    mtime = Column(DateTime, nullable=True)
    parent_reply_id = Column(Integer, nullable=True)

    def __init__(self, article_id, contents, ctime, mtime, parent_reply_id=None):
        self.article_id = article_id
        self.contents = contents
        self.ctime = ctime
        self.mtime = mtime
        self.parent_reply_id = parent_reply_id

    def __str__(self):
        return str(self.__dict__)

class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    user = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __init__(self, user, password):
        self.user = user
        self.password = password

    def __str__(self):
        return str(self.__dict__)



def create_database():
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine

    engine = create_engine('sqlite:///db.sqlite')
    Base.metadata.create_all(engine)


create_database()