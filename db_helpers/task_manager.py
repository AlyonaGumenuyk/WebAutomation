import json
import datetime

from db_helpers.db_helper import DBHelper


class TaskManager(DBHelper):
    def __init__(self):
        super().__init__()

    @staticmethod
    def task_record_to_dict(task_record):
        task_keys = ['id', 'skill', 'arguments', 'attempts', 'worker_type', 'state']
        return dict((zip(task_keys, task_record)))

    @staticmethod
    def task_record_to_task_dict(task_record):
        task_keys = ['task_id', 'skill', 'params', 'worker_type']
        return dict((zip(task_keys, task_record)))

    @staticmethod
    def game_record_to_dict(game_record):
        game_keys = ['id', 'datetime', 'tournament', 'left_command', 'right_command']
        return dict((zip(game_keys, game_record)))

    def get_task_by_task_id(self, task_id):
        query = f"""
            SELECT * from tasks
            WHERE id={task_id}
            """
        if not self.conn:
            self.connect(self.stavka_db)
            self.cur.execute(query)
            record = self.task_record_to_dict(self.cur.fetchone())
            self.close_connection()
        else:
            self.cur.execute(query)
            record = self.task_record_to_dict(self.cur.fetchone())
        return json.dumps(record)

    def get_all_tasks(self, worker_type='all'):
        self.connect(self.stavka_db)
        if worker_type == 'all':
            query = f"""
                SELECT * from tasks
                """
        else:
            query = f"""
                SELECT * from tasks
                WHERE worker_type='{worker_type}'
                """
        self.cur.execute(query)
        records = self.cur.fetchall()
        records_list = []
        for row in records:
            records_list.append(self.task_record_to_dict(row))
        self.close_connection()
        return json.dumps({'tasks': records_list})

    def get_tasks_for_execution(self, worker_type, skill='all', change_task_state=False):
        self.connect(self.stavka_db)
        if skill == 'all':
            if worker_type == 'miner':
                query = f"""
                    SELECT * from tasks
                    WHERE worker_type='{worker_type}'
                    AND state='{self.task_init_state}'
                    """
            elif worker_type == 'better':
                query = f"""
                    SELECT * from tasks
                    WHERE worker_type='{worker_type}'
                    AND state='{self.task_init_state}'
                    LIMIT 1
                    """
            else:
                self.close_connection()
                raise Exception('no such worker type')
        else:
            if worker_type == 'miner':
                query = f"""
                    SELECT * from tasks
                    WHERE worker_type='{worker_type}'
                    AND state='{self.task_init_state}'
                    AND skill='{skill}'
                    """
            elif worker_type == 'better':
                query = f"""
                    SELECT * from tasks
                    WHERE worker_type='{worker_type}'
                    AND state='{self.task_init_state}'
                    AND skill='{skill}'
                    """
            else:
                self.close_connection()
                raise Exception('no such worker type')
        self.cur.execute(query)
        records = self.cur.fetchall()
        records_list = []
        if records:
            for row in records:
                records_list.append(self.task_record_to_task_dict([row[0], row[1], row[2], row[4]]))
                if change_task_state:
                    self.change_task_state(state=self.task_execution_state, task_id=row[0], inc_attempts=False)
            self.close_connection()
        return json.dumps(records_list)

    def get_tournaments(self):
        self.connect(self.stavka_db)
        query = f"""
                SELECT result from results
                WHERE executed_state='success'
                AND skill='get_tournaments'
                ORDER BY id DESC
                LIMIT 1
                """
        self.cur.execute(query)
        tournaments = self.cur.fetchone()
        self.close_connection()
        if tournaments is None:
            tournaments = []
        return json.dumps({'tournaments': json.dumps(tournaments)})

    def get_games(self):
        self.connect(self.stavka_db)
        query = f"""
                SELECT result from results
                WHERE executed_state='success'
                AND skill='get_games'
                """
        self.cur.execute(query)
        games = self.cur.fetchall()
        self.close_connection()
        if games is None:
            tournaments = []
        return json.dumps({'games': games})

    def change_task_state(self, state, task_id, inc_attempts=True):
        task = json.loads(self.get_task_by_task_id(task_id))
        attempts = task["attempts"]
        if inc_attempts:
            attempts = task["attempts"] + 1
        query = f"""
            UPDATE tasks
            SET state='{state}',
                attempts='{attempts}'
            WHERE id={task_id}
            """
        if not self.conn:
            self.connect(self.stavka_db)
            self.cur.execute(query)
            self.conn.commit()
            self.close_connection()
        else:
            self.cur.execute(query)
            self.conn.commit()

    def add_result(self, result, change_task_state=True):
        self.connect(self.stavka_db)
        query = f"""
            INSERT INTO results (task_id, skill, result, executed_state) 
            VALUES ({result["task_id"]}, '{result["skill"]}', 
                    '{json.dumps(result["result"], ensure_ascii=False)}', '{result["executed_state"]}') 
            """
        try:
            self.cur.execute(query)
        except Exception as error:
            print(error)
        self.conn.commit()
        task = json.loads(self.get_task_by_task_id(result['task_id']))
        attempts = task["attempts"]
        state = False
        if change_task_state:
            if result['executed_state'] == 'error' and attempts < 4:
                self.change_task_state(state=self.task_init_state, task_id=result['task_id'])
            else:
                self.change_task_state(state=self.task_complete_state, task_id=result['task_id'])
                state = True
        self.close_connection()
        return state

    def add_games(self, result):
        self.connect(self.stavka_db)
        games = json.loads(result['result'])
        for game in games:
            try:
                game_date_and_time = game['Date of Match'] + '.' + str(datetime.datetime.now().year)[2:] + ' ' + game[
                    'Time of Match']
                game_datetime = datetime.datetime.strptime(game_date_and_time, '%d.%m.%y %H:%M')
                game_tournament = game['Tournament name']
                game_left_command = game['Left command name']
                game_right_command = game['Right command name']

                query = f"""
                        INSERT INTO games (datetime, tournament, left_command, right_command) 
                        SELECT to_timestamp('{game_datetime}', 'yyyy-mm-dd hh24:mi:ss'), 
                                '{game_tournament}', '{game_left_command}', '{game_right_command}'
                        WHERE NOT EXISTS (SELECT 1 FROM games
                                          WHERE datetime='{game_datetime}'
                                          AND tournament='{game_tournament}'
                                          AND left_command='{game_left_command}'
                                          AND right_command='{game_right_command}')
                        """
                self.cur.execute(query)
            except Exception as error:
                print(error)
            self.conn.commit()
        self.close_connection()

    def get_games_to_create_tasks(self):
        self.connect(self.stavka_db)
        try:
            task_datetime_minus_minute = datetime.datetime.now() - datetime.timedelta(minutes=1)
            time_to_create_task = task_datetime_minus_minute.strftime('%y-%m-%d %H:%M')
            query = f"""
                    SELECT * FROM games
                    WHERE datetime = to_timestamp('{time_to_create_task}', 'yy-mm-dd hh24:mi:ss')
                    """
            self.cur.execute(query)
            games = self.cur.fetchall()
            if not games:
                raise Exception
            games_list = []
            for game in games:
                games_list.append(self.game_record_to_dict(game))
            return games_list
        except:
            return None
        finally:
            self.close_connection()
