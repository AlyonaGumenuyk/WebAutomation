import json

from flask import Flask, jsonify, make_response, request, Response, stream_with_context
from flask_restful import Resource, Api

from client.better import Better
from server.better_starter import BetterStarter
from task_management.better_task_manager import BetterTaskManeger
from task_management.miner_task_manager import MinerTaskManeger
from server.mainer_starter import MainerStarter
from task_management.task_queue import TaskQueue

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
api = Api(app)


task_manager = BetterTaskManeger()
mainer_starter = MainerStarter(task_manager.task_queue)
# better_starter = BetterStarter(task_manager.task_queue)


class IndexPage(Resource):
    @staticmethod
    def get():
        # task_manager.run()
        return 0


class CheckTaskQueue(Resource):
    @staticmethod
    def get():
        result = []
        for item in task_manager.task_queue.queue:
            result.append(item)
        return make_response(jsonify(result))


class BetterGetCoefs(Resource):
    @staticmethod
    def get():
        with open('task_report/gamestat.json', 'r') as gamestat:
            return make_response(json.load(gamestat))

    @staticmethod
    def post():
        if request.is_json:
            data = request.get_json()
            with open('task_report/gamestat.json', 'w') as current_stat:
                current_stat.seek(0)
                current_stat.truncate()
                json.dump(data, current_stat, indent=4)


api.add_resource(IndexPage, '/')
api.add_resource(CheckTaskQueue, '/tasks')
api.add_resource(BetterGetCoefs, '/get_coefs')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=True, use_reloader=False)
