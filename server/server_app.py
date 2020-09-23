import json
import os
import platform
import time

from flask import Flask, make_response, request
from flask_restful import Resource, Api

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
            current_tasks.seek(0)
            current_tasks.truncate()
            json.dump(data, current_tasks, indent=4)


update_tasks(['miner', 'better'])

better_task_manager = BetterTaskManager()
time.sleep(1)
miner_task_manager = MinerTaskManager()

# miner_starter = MinerStarter()
# better_starter = BetterStarter()


class IndexPage(Resource):
    @staticmethod
    def get():
        return 0


class GetTasks(Resource):
    @staticmethod
    def get():
        with open('task_report/tasks.json', encoding='utf8') as current_tasks:
            try:
                return make_response(json.load(current_tasks))
            except json.decoder.JSONDecodeError:
                return make_response(json.loads(json.dumps(dict({'Error': 'empty file'}))))

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
            try:
                return make_response(json.load(tournaments))
            except json.decoder.JSONDecodeError:
                return make_response(json.loads(json.dumps(dict({'Error': 'empty file'}))))

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
            try:
                result = json.load(games)
                return make_response(result)
            except json.decoder.JSONDecodeError:
                return make_response(json.loads(json.dumps(dict({'Error': 'empty file'}))))

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
            try:
                return make_response(json.load(gamestat))
            except json.decoder.JSONDecodeError:
                return make_response(json.loads(json.dumps(dict({'Error': 'empty file'}))))

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
            try:
                return make_response(json.load(report))
            except json.decoder.JSONDecodeError:
                return make_response(json.loads(json.dumps(dict({'Error': 'empty file'}))))

    @staticmethod
    def post():
        if request.is_json:
            data = request.get_json()
            with open('task_report/report.json', 'r+', encoding='utf8') as report:
                try:
                    report_dict = json.load(report)
                    report.seek(0)
                    report.truncate()
                    report_dict["report"].insert(0, data)
                except json.decoder.JSONDecodeError:
                    report_dict = dict({"report": [data]})
                json.dump(report_dict, report, indent=4)


api.add_resource(IndexPage, '/')
api.add_resource(GetTasks, '/tasks')
api.add_resource(MinerGetTournaments, '/tournaments')
api.add_resource(MinerGetGames, '/games')
api.add_resource(BetterGetCoefs, '/get_coefs')
api.add_resource(Report, '/report')

if __name__ == '__main__':
    if platform.system() == "Windows":
        host = '127.0.0.1'
        port = 8000
    else:
        host = '0.0.0.0'
        port = 8080
    app.run(host=host, port=port, debug=True, use_reloader=False)
