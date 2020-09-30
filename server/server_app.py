import json
import os
import platform

from flask import Flask, make_response, request
from flask_restful import Resource, Api

from db_helpers.task_manager import TaskManager

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
api = Api(app)

task_manager = TaskManager()


class IndexPage(Resource):
    @staticmethod
    def get():
        return 0


class GetTasks(Resource):
    @staticmethod
    def get():
        try:
            tasks = task_manager.get_all_tasks()
            return make_response(json.loads(tasks))
        except Exception as error:
            return make_response(json.loads(json.dumps(dict({'error': str(error).strip()}))))

    @staticmethod
    def post():
        try:
            if request.is_json:
                request_data = request.get_json()
                tasks = task_manager.get_tasks_for_execution(worker_type=request_data['worker_type'],
                                                             change_task_state=True)
                return json.loads(tasks)
        except Exception as error:
            return json.loads(json.dumps(dict({'error': str(error).strip()})))


class MinerGetTournaments(Resource):
    @staticmethod
    def get():
        try:
            tournaments = task_manager.get_tournaments()
            return make_response(json.loads(tournaments))
        except Exception as error:
            return make_response(json.loads(json.dumps(dict({'error': str(error).strip()}))))

    @staticmethod
    def post():
        try:
            if request.is_json:
                result = request.get_json()
                task_manager.add_result(result)
        except Exception as error:
            return make_response(json.dumps(dict({'error': str(error).strip()})))


class MinerGetGames(Resource):
    @staticmethod
    def get():
        try:
            games = task_manager.get_games()
            return make_response(json.loads(games))
        except Exception as error:
            return make_response(json.loads(json.dumps(dict({'error': str(error).strip()}))))

    @staticmethod
    def post():
        try:
            if request.is_json:
                result = request.get_json()
                task_state = task_manager.add_result(result)
                if task_state:
                    task_manager.add_games(result)
        except Exception as error:
            return make_response(json.dumps(dict({'error': str(error).strip()})))


class BetterWatch(Resource):
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
api.add_resource(BetterWatch, '/watch')
api.add_resource(Report, '/report')

if __name__ == '__main__':
    if platform.system() == "Windows":
        host = '127.0.0.1'
        port = 8000
    else:
        host = '0.0.0.0'
        port = 8080
    app.run(host=host, port=port, debug=True, use_reloader=False)
