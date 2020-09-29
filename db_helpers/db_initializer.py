from psycopg2 import connect, extensions, sql, errors, DatabaseError

from db_helpers.db_helper import DBHelper


class DBInitializer(DBHelper):

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

            except errors.DuplicateDatabase:
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
                                CREATE TABLE results (id SERIAL, task_id int, skill varchar(20),
                                result json, executed_state varchar(20))
                                """
                self.cur.execute(create_results_query)

                create_games_query = """
                                CREATE TABLE games (id SERIAL, datetime timestamp, tournament text,
                                                    left_command text, right_command text)
                                """
                self.cur.execute(create_games_query)

                self.conn.commit()
                print("Tables created successfully in " + str(self.stavka_db))
            except (Exception, DatabaseError) as error:
                print("Error while creating tables in " + str(self.stavka_db), error)
            finally:
                self.close_connection()
