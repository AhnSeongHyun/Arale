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
    pid = Column(Integer, nullable=True)
    contents = Column(Text, nullable=True)
    ctime = Column(DateTime, nullable=False)

    def __init__(self, title, contents, ctime, mtime):
        self.title = title
        self.contents = contents
        self.ctime = ctime
        self.mtime = mtime

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