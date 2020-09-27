from psycopg2 import connect, extensions, sql, errors, DatabaseError


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

    def insert_into_tasks(self, skill, arguments, worker_type, created, access_after):
        self.connect()
        if self.conn:
            try:
                task = f"""
                INSERT INTO tasks (skill, arguments, attempts, worker_type, created, access_after) 
                VALUES ('{skill}', '{arguments}', 0, {worker_type}, '{created}',
                '{access_after}') RETURNING id
                """
                self.cur.execute(postgres_insert_query, record_to_insert)
                self.conn.commit()
            except (Exception, errors) as error:
                print("Failed to insert record into mobile table", error)
            finally:
                self.close_connection()

    def task_generation(self):
        self.connect()
        if self.conn:
            while True:
                tournaments


