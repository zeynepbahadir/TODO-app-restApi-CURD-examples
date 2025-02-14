import json
import sqlite3
from sqlite3 import Error
import bson


class SqlOperation:

    def __init__(self):
        """Initialize database connection."""
        self.db_path = "todoDB.db"
        try:
            conn_ = sqlite3.connect(self.db_path, check_same_thread=False)
            print("sqlite3 version is:", sqlite3.version)
        except Error as e:
            print(f"Failed to connect to database: {e}")
            raise
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
            print(f"Failed to creata table: {e}")
            raise

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
            print(f"Failed to selecting all tasks from database: {e}")
            raise

    def add_task(self, task_):
        sql = ''' INSERT INTO tasks(id, content, status)
                  VALUES(?,?,?)'''
        try:
            cur = self.conn_.cursor()
            cur.execute(sql, task_)
            self.conn_.commit()
            return cur.lastrowid
        except Error as e:
            print(f"Failed to adding task to database: {e}")
            raise

    def get_task(self, id_):
        sql = "SELECT * FROM tasks WHERE id = ?"
        try:
            cur = self.conn_.cursor()
            cur.execute(sql, (id_,))
            gtask = cur.fetchone()
            print(gtask)
            return gtask
        except Error as e:
            print(f"Failed to selecting task from database: {e}")
            raise

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
            print(f"Failed to update task: {e}")
            raise

    def delete_task(self, id_):
        sql = 'DELETE FROM tasks WHERE id = ?'
        try:
            cur = self.conn_.cursor()
            cur.execute(sql, (id_,))
            self.conn_.commit()
        except Error as e:
            print(f"Failed to deleting task from database: {e}")
            raise
