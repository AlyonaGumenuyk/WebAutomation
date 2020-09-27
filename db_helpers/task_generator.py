import json
import time

from psycopg2 import connect, extensions, sql, errors, DatabaseError

from task_management.task import Task

TASK_WAITING = 'waiting for execution'
TASK_EXECUTING = 'executing'
TASK_COMPLETED = 'execution completed'


class TaskGenerator:
    def __init__(self):
        self.stavka_db = '1xStavkaDB'
        self.user = 'postgres'
        self.host = 'localhost'
        self.password = 'boss1234'
        self.conn = None
        self.cur = None
        self.tournaments_delay = 60 * 60 * 24
        self.games_delay = 60 * 60 * 12
        self.task_generation()

    def connect(self):
        try:
            self.conn = connect(
                dbname=self.stavka_db,
                user=self.user,
                host=self.host,
                password=self.password
            )
            self.cur = self.conn.cursor()
            print('Connected to ' + str(self.stavka_db))
        except Exception as error:
            print('Error while connecting to PostgreSQL: ', str(error).strip())

    def close_connection(self):
        if self.conn:
            self.cur.close()
            self.conn.close()
            print('Connection closed')

    def insert_into_tasks(self, skill, arguments, attempts, worker_type, state):
        self.connect()
        if self.conn:
            try:
                task = f"""
                INSERT INTO tasks (skill, arguments, attempts, worker_type, state) 
                VALUES ('{skill}', '{arguments}', {attempts}, '{worker_type}', '{state}')
                """
                self.cur.execute(task)
                self.conn.commit()
                print('Task has been inserted')
            except Exception as error:
                print("Failed to insert record into tasks table", error)
            finally:
                self.close_connection()

    def task_generation(self):
        while True:
            tournaments_task = self.get_tournaments_task('Football')
            self.insert_into_tasks(skill=tournaments_task.method, arguments=json.dumps(tournaments_task.params),
                                   attempts=0, worker_type=tournaments_task.worker_type, state=TASK_WAITING)
            time.sleep(600)

    @classmethod
    def get_tournaments_task(cls, sport_name):
        return Task('get_tournaments', [sport_name], 'miner')

    @classmethod
    def get_games_task(cls, tournament_url):
        return Task('get_games', [tournament_url], 'miner')

    @classmethod
    def get_watch_task(cls, game_url):
        return Task('watch', [game_url], 'better')
