from psycopg2 import connect, extensions, sql, errors, DatabaseError


class DBManager:

    def __init__(self):
        self.init_db = 'postgres'
        self.user = 'postgres'
        self.host = 'localhost'
        self.password = 'boss1234'
        self.conn = None
        self.cur = None
        self.stavka_db = '1xStavkaDB'

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

    def create_db(self):
        self.connect(self.init_db)
        if self.conn:
            try:
                autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
                self.conn.set_isolation_level(autocommit)
                self.cur.execute(sql.SQL("""CREATE DATABASE {}
                                                LOCALE 'en_US.UTF-8'
                                                TEMPLATE template0""").format(sql.Identifier(self.stavka_db)))
                print('Created ' + str(self.stavka_db))

            except errors.DuplicateDatabase as error:
                print('1xStavkaDB is already exists')

            except Exception as error:
                print('Error while creating db ', str(error).strip())

            finally:
                self.close_connection()

    def create_tables(self):
        self.connect(self.stavka_db)
        if self.conn:
            try:
                create_tasks_query = """
                CREATE TABLE tasks (id SERIAL, skill varchar(20), arguments json,
                attempts smallint, worker_type varchar(20), state varchar(30))
                """
                self.cur.execute(create_tasks_query)

                create_results_query = """
                CREATE TABLE results (id SERIAL, task_id int, skill varchar(20), result text)
                """
                self.cur.execute(create_results_query)

                self.conn.commit()
                print("Tables created successfully in " + str(self.stavka_db))
            except (Exception, DatabaseError) as error:
                print("Error while creating tables in " + str(self.stavka_db), error)
            finally:
                self.close_connection()
