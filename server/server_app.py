from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api

from task_management.task_manager import TaskManeger
from server.mainer_starter import MainerStarter

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
api = Api(app)

task_manager = TaskManeger()
mainer_starter = MainerStarter(task_manager.task_queue)


class IndexPage(Resource):
    @staticmethod
    def get():
        result = task_manager.work()
        return result


class CheckTaskQueue(Resource):
    @staticmethod
    def get():
        result = []
        for item in task_manager.task_queue.queue:
            result.append(item)
        return make_response(jsonify(result))


api.add_resource(IndexPage, '/')
api.add_resource(CheckTaskQueue, '/tasks')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=True, use_reloader=False)
