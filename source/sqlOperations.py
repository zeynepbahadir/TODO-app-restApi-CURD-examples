import sqlite3
from sqlite3 import Error
from typing import List, Dict

class SqlOperation:

    def __init__(self, db_path):
        """Initialize database connection."""
        self.db_path = db_path #"todoDB.db"
        try:
            conn_ = sqlite3.connect(self.db_path, check_same_thread=False)
            print("sqlite3 version is:", sqlite3.version)
        except Error as e:
            print(f"Failed to connect to database: {e}")
            raise
        self.conn_ = conn_

    def generate_unique_id(self) -> int:
        """Generate a unique ID for a new task.
        
        Returns:
            int: New unique ID (last ID + 1 or 1 if table is empty)
        """
        try:
            cur = self.conn_.cursor()
            # Get the maximum ID currently in use
                                                    #TODO add reusable function 
            cur.execute("SELECT MAX(id) FROM tasks")
            result = cur.fetchone()[0]
            # If table is empty, start with 1, else increment the max id
            return 1 if result is None else result + 1
        except Error as e:
            print(f"Failed to generate unique ID: {e}")
            raise

    def create_table(self) -> None:
        """Create a table named 'tasks' with the columns 'id', 'content', 'status'."""
        sql = """ CREATE TABLE IF NOT EXISTS tasks (            
                                        id INTEGER PRIMARY KEY,
                                        content TEXT NOT NULL,
                                        status BOOLEAN NOT NULL DEFAULT FALSE
                                    );"""
        try:
            cur = self.conn_.cursor()
            cur.execute(sql)
        except Error as e:
            print(f"Failed to creata table: {e}")
            raise

    def select_all_tasks(self) -> List:
        """Creating and returning all the task list."""
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

    def add_task(self, task_) -> None:
        """Adding a new task to database."""
        #sql = ''' INSERT INTO tasks(id, content, status)
        sql = ''' INSERT INTO tasks(id, content, status)
                  VALUES(?,?,?)'''
        try:
            id = self.generate_unique_id()
            cur = self.conn_.cursor()
            cur.execute(sql, (id, task_, False))
            self.conn_.commit()
            return cur.lastrowid
        except Error as e:
            print(f"Failed to adding task to database: {e}")
            raise

    def get_task(self, id_) -> Dict:
        """Fetching a spesific task with the given id."""
        sql = "SELECT * FROM tasks WHERE id = ?"
        try:
            cur = self.conn_.cursor()
            cur.execute(sql, (id_,))
            gtask = cur.fetchone()
            return gtask
        except Error as e:
            print(f"Failed to selecting task from database: {e}")
            raise

    def update_task(self, id_) -> None:
        """Update a tasks status between 0-1. (done - not done)"""
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

    def delete_task(self, id_) -> None:
        """Delete a task with the given id."""
        sql = 'DELETE FROM tasks WHERE id = ?'
        try:
            cur = self.conn_.cursor()
            cur.execute(sql, (id_,))
            self.conn_.commit()
        except Error as e:
            print(f"Failed to deleting task from database: {e}")
            raise

    def fetch_last_id(self) -> int:
        """Finds the id of the last row."""
        cur = self.conn_.cursor()
        cur.execute("SELECT MAX(id) FROM tasks")
        result = cur.fetchone()[0]
        #x = cur.execute("select * from tasks order by id DESC limit 1;").fetchone()
        return result
    