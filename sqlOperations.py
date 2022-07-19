import json
import sqlite3
from sqlite3 import Error
import bson


class SqlOperation:

    def __init__(self):
        self.db_path = "/home/zeynep/py/todoDB.db"
        try:
            conn_ = sqlite3.connect(self.db_path, check_same_thread=False)
            print("sqlite3 version is:", sqlite3.version)
        except Error as e:
            print(e)
        self.conn_ = conn_

    def create_table(self):
        sql = """ CREATE TABLE IF NOT EXISTS tasks (
                                        id integer,
                                        content text,
                                        status bool
                                    );"""
        try:
            cur = self.conn_.cursor()
            cur.execute(sql)
        except Error as e:
            print(e)

    def select_all_tasks(self):
        mlist = []
        try:
            cur = self.conn_.cursor()
            cur.execute("SELECT * FROM tasks")
            rows = cur.fetchall()

            for row in rows:
                #print(row)
                mlist.append(row)
            return mlist
        except Error as e:
            print(e)

    def add_task(self, task_):
        sql = ''' INSERT INTO tasks(id, content, status)
                  VALUES(?,?,?)'''
        try:
            cur = self.conn_.cursor()
            cur.execute(sql, task_)
            self.conn_.commit()
            return cur.lastrowid
        except Error as e:
            print(e)

    def get_task(self, id_):
        sql = "SELECT * FROM tasks WHERE id = ?"
        try:
            cur = self.conn_.cursor()
            cur.execute(sql, (id_,))
            gtask = cur.fetchone()
            print(gtask)
            return gtask
        except Error as e:
            print(e)

    def update_task(self, id_):
        sql1 = "SELECT * FROM tasks WHERE id = ?"
        sql2 = '''UPDATE tasks
                SET status = ?
                WHERE id = ?'''
        try:
            cur = self.conn_.cursor()
            cur.execute(sql1, (id_,))
            mtask = cur.fetchone()
            #print("mtask:", mtask)
            mstatus = 0
            if mtask[2] == 0:
                mstatus = 1
            #print("mstatus: ", mstatus)
            cur.execute(sql2, (mstatus, id_))
            self.conn_.commit()
            #print("changed the status of the task ", id_)
        except Error as e:
            print(e)

    def delete_task(self, id_):
        sql = 'DELETE FROM tasks WHERE id = ?'
        try:
            cur = self.conn_.cursor()
            cur.execute(sql, (id_,))
            self.conn_.commit()
        except Error as e:
            print(e)

    '''
    conn = create_connection(db_path)
    
    if conn is not None:
        create_table(conn)
        with conn:
            #print("adding task.............")
            #task = (3, 'todo1', False)
            #create_todo(conn, task)
    
            print("all tasks:")
            select_all_tasks(conn)
    
            #print("updating task...........")
            #StatusAndID = (True, 2)
            #update_task(conn, StatusAndID)
    
    
            #print("deleting task............")
            #deleteID = 3
            #delete_task(conn, deleteID)
    
    
            #select_all_tasks(conn)
    else:
        print("Error! Cannot create Database")
    '''