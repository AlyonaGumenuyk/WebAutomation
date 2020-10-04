import json
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


class GetTournaments(Resource):
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


class GetGames(Resource):
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
    def post():
        try:
            if request.is_json:
                result = request.get_json()
                if result['result'] != 'finished':
                    if result['executed_state'] == 'success':
                        task_manager.add_result(result, change_task_state=False)
                    else:
                        if result['result'] == 'No tournament with such name' \
                                or result['result'] == 'No match with such command names':
                            task_manager.add_result(result, change_task_state=False, complete_execution=True)
                        else:
                            task_manager.add_result(result)
                else:
                    task_manager.add_result(result)
        except Exception as error:
            return make_response(json.dumps(dict({'error': str(error).strip()})))


class GetResult(Resource):
    @staticmethod
    def get():
        try:
            result = task_manager.get_result()
            return make_response(json.loads(result))
        except Exception as error:
            return make_response(json.loads(json.dumps(dict({'error': str(error).strip()}))))


api.add_resource(IndexPage, '/')
api.add_resource(GetTasks, '/tasks')
api.add_resource(GetTournaments, '/tournaments')
api.add_resource(GetGames, '/games')
api.add_resource(BetterWatch, '/watch')
api.add_resource(GetResult, '/result')

if __name__ == '__main__':
    if platform.system() == "Windows":
        host = '127.0.0.1'
        port = 8000
    else:
        host = '0.0.0.0'
        port = 8000
    app.run(host=host, port=port, debug=True, use_reloader=False)
