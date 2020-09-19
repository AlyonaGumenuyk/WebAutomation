import json
import os
import time

from flask import Flask, make_response, request
from flask_restful import Resource, Api

from server.better_starter import BetterStarter
from server.miner_starter import MinerStarter
from task_management.better_task_manager import BetterTaskManager
from task_management.miner_task_manager import MinerTaskManager

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
api = Api(app)


def update_tasks(workers_list):
    with open('task_report/tasks.json', 'r+', encoding='utf8') as current_tasks:
        try:
            data = json.load(current_tasks)
            for worker in workers_list:
                data.update({worker: []})
                current_tasks.seek(0)
                current_tasks.truncate()
                json.dump(data, current_tasks, indent=4)
        except:
            data = dict({'miner': [], 'better': []})
            json.dump(data, current_tasks, indent=4)


update_tasks(['miner', 'better'])

better_task_manager = BetterTaskManager()
miner_task_manager = MinerTaskManager()

miner_starter = MinerStarter()
# better_starter = BetterStarter()


class IndexPage(Resource):
    @staticmethod
    def get():
        return 0


class GetTasks(Resource):
    @staticmethod
    def get():
        with open('task_report/tasks.json', encoding='utf8') as current_tasks:
            return make_response(json.load(current_tasks))

    @staticmethod
    def post():
        if request.is_json:
            request_data = request.get_json()
            with open('task_report/tasks.json', encoding='utf8') as current_tasks:
                data = json.load(current_tasks)
            if request_data['worker_type'] == 'miner':
                tasks = json.loads(json.dumps(data['miner']))
                update_tasks(['miner'])
                return tasks
            elif request_data['worker_type'] == 'better':
                tasks = json.loads(json.dumps(data['better']))
                update_tasks(['better'])
                return tasks


class MinerGetTournaments(Resource):
    @staticmethod
    def get():
        with open('task_report/tournaments.json', 'r', encoding='utf8') as tournaments:
            return make_response(json.load(tournaments))

    @staticmethod
    def post():
        if request.is_json:
            data = request.get_json()
            with open('task_report/tournaments.json', 'w', encoding='utf8') as tournaments:
                tournaments.seek(0)
                tournaments.truncate()
                json.dump(data, tournaments, indent=4, ensure_ascii=False)
                with open('task_report/games.json', 'r+', encoding='utf8') as games:
                    if os.path.getsize('task_report/games.json') > 0:
                        games.seek(0)
                        games.truncate()


class MinerGetGames(Resource):
    @staticmethod
    def get():
        with open('task_report/games.json', 'r', encoding='utf8') as games:
            result = json.load(games)
            return make_response(result)

    @staticmethod
    def post():
        if request.is_json:
            data = request.get_json()
            with open('task_report/games.json', 'r+', encoding='utf8') as games:
                if os.path.getsize('task_report/games.json') > 0:
                    current_games = json.load(games)
                    games.seek(0)
                    games.truncate()
                    print(data)
                    current_games.update(data)
                else:
                    current_games = data
                json.dump(current_games, games, indent=4, ensure_ascii=False)


class BetterGetCoefs(Resource):
    @staticmethod
    def get():
        with open('task_report/gamestat.json', 'r', encoding='utf8') as gamestat:
            return make_response(json.load(gamestat))

    @staticmethod
    def post():
        if request.is_json:
            data = request.get_json()
            with open('task_report/gamestat.json', 'w', encoding='utf8') as current_stat:
                current_stat.seek(0)
                current_stat.truncate()
                json.dump(data, current_stat, indent=4)


class Report(Resource):
    @staticmethod
    def get():
        with open('task_report/report.json', 'r', encoding='utf8') as report:
            return make_response(json.load(report))

    @staticmethod
    def post():
        if request.is_json:
            data = request.get_json()
            with open('task_report/report.json', 'r+', encoding='utf8') as report:
                if os.path.getsize('task_report/report.json') > 0:
                    current_games = json.load(report)
                    report.seek(0)
                    report.truncate()
                    current_games.append(data)
                else:
                    current_games = [data]
                json.dump(current_games, report, indent=4)


api.add_resource(IndexPage, '/')
api.add_resource(GetTasks, '/tasks')
api.add_resource(MinerGetTournaments, '/tournaments')
api.add_resource(MinerGetGames, '/games')
api.add_resource(BetterGetCoefs, '/get_coefs')
api.add_resource(Report, '/report')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=True, use_reloader=False)
