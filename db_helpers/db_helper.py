import json

from psycopg2 import connect, extensions, sql, errors, DatabaseError


class DBHelper:

    def __init__(self):
        # self.user = 'docker'
        # self.host = '172.18.0.1'
        # self.password = 'docker'
        self.user = 'postgres'
        self.host = 'localhost'
        self.password = 'boss1234'
        self.conn = None
        self.cur = None
        self.stavka_db = '1xStavkaDB'
        self.task_init_state = 'waiting for execution'
        self.task_execution_state = 'currently executing'
        self.task_complete_state = 'execution completed'
        self.conn_retry_delay = 10
        self.task_max_attempts = 5

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
        if not self.conn:
            raise Exception
        if self.conn:
            try:
                query = """
                INSERT INTO tasks (skill, arguments, attempts, worker_type, state)
                VALUES (%s,%s,%s,%s,%s)
                """
                record_to_insert = (skill, json.dumps(arguments, ensure_ascii=False), attempts, worker_type, state)
                self.cur.execute(query, record_to_insert)
                self.conn.commit()
                print('Task has been inserted')
            except Exception as error:
                print("Failed to insert record into tasks table", error)
            finally:
                self.close_connection()
