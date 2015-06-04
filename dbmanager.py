# -*- coding:utf-8 -*-

import datetime
import traceback

from sqlalchemy import create_engine, desc 
from mapper import *
from sqlalchemy import func 

CONNECTION_STRING = 'sqlite:///db/db.sqlite'

class OrmManager(object):

    mssql_session = None  

    def open(self):
        try:
            engine = create_engine(CONNECTION_STRING)
            Session = sessionmaker(bind=engine) 
            self.mssql_session = Session()
        except Exception as e:
            raise e

    def insert_new(self, data): #top level new article
        pid = 0
        gid = self.get_max_gid() +1 
        gorder = 0
        level = 0
        try: 
            self.insertBoard(Board(data['email'], data['password'], data['title'], data['article'], \
                datetime.datetime.now(), None, pid, gid, gorder, level))
        except Exception as e:
            raise e


    def insert_reply(self, data):
        ppid = int(data['ppid'])
        if ppid == 0:
            new_gorder = self.get_max_gorder_by_gid(int(data['gid']))+1
        else:
            new_gorder = int(data['gorder']) + 1

        try: 
            inserted_id = self.insertBoard(Board(data['email'],data['password'], data['title'], data['article'], \
                datetime.datetime.now(), None, int(data['pid']), int(data['gid']), new_gorder, int(data['level'])+1))

            same_over_board_ids = self.same_over_gorder_in_gid(new_gorder, int(data['gid']), inserted_id)
            if same_over_board_ids.count > 0:
                self.increase_gorder(same_over_board_ids)

        except Exception as e:
            raise e



    def same_over_gorder_in_gid(self, new_gorder, gid, except_id):
        self.open()
        result = self.mssql_session.query(Board.id).filter(Board.gid==gid).\
        filter(Board.gorder>=new_gorder).\
        filter(Board.id!=except_id).all()
        self.close()
        return result

    def increase_gorder(self, same_over_board_ids):
        self.open()
        for bd_id in same_over_board_ids: 
            board = self.mssql_session.query(Board).filter(Board.id==bd_id[0]).one()
            board.gorder +=1

        self.mssql_session.commit()
        self.close()


    def get_max_gorder_by_gid(self, gid):
        self.open()
        result = self.mssql_session.query(func.max(Board.gorder)).filter(Board.gid==gid).scalar()
        self.close()

        if not result:
            return 0
        return result 


    def get_max_gid(self):
        self.open()
        result = self.mssql_session.query(func.max(Board.gid)).scalar()
        self.close()

        if not result:
            return 0
        return result 

    def insertBoard(self, board):
        try:
            self.open()
            self.mssql_session.add(board)
            self.mssql_session.commit()
            self.mssql_session.refresh(board)
            return board.id 
        except Exception as e:
            self.close()
            raise e

    def update(self, id, data):
        try:
            self.open()
            board = self.mssql_session.query(Board).filter(Board.id==id).one()
            board.email = data['email'] 
            board.title = data['title']
            board.article = data['article']
            board.mtime = datetime.datetime.now()
            self.mssql_session.commit()
            result = self.mssql_session.query(Board).filter(Board.id==id).one()
            self.close()
            return result 
        except Exception as e:
            self.close()
            raise e 
 

    def select(self, start_index, paging_size):
        try:
            self.open()
            q = self.mssql_session.query(Board).order_by(desc(Board.gid)).order_by(Board.gorder)
            q = q.offset(start_index)
            q = q.limit(paging_size) 
            top_level = q
            self.close()
            return top_level
        except Exception as e:
            self.close()
            raise e  
 

    def select_by_id(self, id):

        try:
            self.open()
            result = self.mssql_session.query(Board).filter(Board.id==id).one()

        except Exception as e:
            self.close()
            raise e  

        try:
            if result.pid and result.pid!=-1: #get parent_id 
                result.parent = self.mssql_session.query(Board).filter(Board.id==result.pid).one()

        except Exception as e:
            self.close()
            
        finally:
            self.close()
            return result
    

    def count(self):
        try:
            self.open()
            total_count = self.mssql_session.query(func.count(Board.id)).scalar()
            return total_count
        except Exception as e:
            self.close()
            raise e  


    def delete(self, id):
        try:
            self.open()
            
            for sub_borad in self.mssql_session.query(Board).filter(Board.pid==id):
                sub_borad.pid =-1

            result = self.mssql_session.query(Board).filter(Board.id==id).one()

            
            self.mssql_session.delete(result)
            self.mssql_session.commit()

        except Exception as e:
            self.close()
            raise e
        

    def close(self):
        if self.mssql_session:
                self.mssql_session.close()

 