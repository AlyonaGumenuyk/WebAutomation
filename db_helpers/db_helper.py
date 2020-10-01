import json

from psycopg2 import connect, extensions, sql, errors, DatabaseError


class DBHelper:

    def __init__(self):
        self.init_db = 'postgres'
        self.user = 'postgres'
        self.host = 'localhost'
        self.password = 'boss1234'
        self.conn = None
        self.cur = None
        self.stavka_db = '1xStavkaDB'
        self.task_init_state = 'waiting for execution'
        self.task_execution_state = 'currently executing'
        self.task_complete_state = 'execution completed'
        self.result_relevance_relevant_state = 'relevant'
        self.result_relevance_outdated_state = 'outdated'

    def connect(self, db_to_connect_name):
        try:
            self.conn = connect(
                dbname=db_to_connect_name,
                user=self.user,
                host=self.host,
                password=self.password
            )
            self.cur = self.conn.cursor()
            print('Connected to ' + str(db_to_connect_name))
        except Exception as error:
            print('Error while connecting to PostgreSQL: ', str(error).strip())

    def close_connection(self):
        if self.conn:
            self.cur.close()
            self.conn.close()
            print('Connection closed')

    def insert_into_tasks(self, skill, arguments, attempts, worker_type, state):
        self.connect(self.stavka_db)
        if self.conn:
            try:
                task = f"""
                INSERT INTO tasks (skill, arguments, attempts, worker_type, state) 
                VALUES ('{skill}', '{json.dumps(arguments, ensure_ascii=False)}', {attempts}, '{worker_type}', '{state}')
                """
                self.cur.execute(task)
                self.conn.commit()
                print('Task has been inserted')
            except Exception as error:
                print("Failed to insert record into tasks table", error)
            finally:
                self.close_connection()
