import json

from psycopg2 import connect, extensions, sql, errors, DatabaseError


class DBHelper:

    def __init__(self):
        self.user = 'docker'
        # self.user = 'postgres'
        self.host = '172.17.0.1'
        # self.host = 'localhost'
        self.password = 'docker'
        # self.password = 'boss1234'
        self.conn = None
        self.cur = None
        self.stavka_db = '1xStavkaDB'
        self.task_init_state = 'waiting for execution'
        self.task_execution_state = 'currently executing'
        self.task_complete_state = 'execution completed'
        self.task_timeout_state = 'timeout exceeded'
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
        except Exception as error:
            print(repr(error))

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
            except Exception as err:
                print(repr(err))
                pass
            finally:
                self.close_connection()

    def update_timeout(self):
        self.connect(self.stavka_db)
        if not self.conn:
            raise Exception
        if self.conn:
            try:
                query = f"""
                    UPDATE tasks
                    SET state='{self.task_timeout_state}'
                    WHERE created_at + (3 ||' hours')::interval < now()
                    AND state='waiting for execution'
                    OR state='currently executing'
                    """
                self.cur.execute(query)
                self.conn.commit()
            except Exception as error:
                pass
            finally:
                self.close_connection()
