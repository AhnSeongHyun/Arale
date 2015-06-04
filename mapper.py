import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

import datetime
Base = declarative_base()

class Board(Base):
    __tablename__ = 'board'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    title = Column(Text, nullable=False)
    article = Column(Text, nullable=True)
    ctime = Column(DateTime, nullable=False)
    mtime = Column(DateTime, nullable=True)
    gid = Column(Integer)
    pid = Column(Integer)
    gorder = Column(Integer)
    level =  Column(Integer)
 


    def __init__(self, email, password, title, article, ctime, mtime, pid, gid, gorder, level):
        self.email = email
        self.password = password
        self.title = title
        self.article = article
        self.ctime = ctime 
        self.mtime = mtime
        self.pid = pid
        self.gid = gid
        self.gorder = gorder
        self.level = level 
        

    def __str__(self):
        return str(self.__dict__)



    #For HTML 
    @property 
    def email_html(self):
        return self.email.split('@')[0]

    @property
    def ctime_html(self):
        return self.ctime.strftime("%Y-%m-%d %H:%M:%S")

    
    @property
    def title_html(self):
        html=''

        now = datetime.datetime.now()
        margin = datetime.timedelta(minutes = 30)
       
        if now-margin <= self.ctime <= now:
            html='<button type="button" class="btn btn-danger btn-xs">New</button>&nbsp;'

        if self.pid != 0:
            html += ('&nbsp;'*self.level)+'<a href=/articles/'+str(self.id)+'>'
            html +='[RE] '
        else:
            html += '<a href=/articles/'+str(self.id)+'>'


        html += self.title+'</a>'

        return  html


if __name__ == '__main__':
    engine = create_engine('mssql+pyodbc://@localhost\SQLEXPRESS/BRAAVOS')
    Base.metadata.create_all(engine)