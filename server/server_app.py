from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api

from client.better import Better
from task_management.task_manager import TaskManeger
from server.mainer_starter import MainerStarter
from task_management.task_queue import TaskQueue

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
api = Api(app)


# task_manager = TaskManeger()
# mainer_starter = MainerStarter(task_manager.task_queue)


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
        queue = TaskQueue()
        better = Better(queue)
        result = better.get_coefs(
            'https://1xstavka.ru/en/live/Football/2103135-USSR-3x3-Division-B/256329132-Georgia-3h3-Ukraine-3h3/')
        better.driver.close()
        return make_response(result)


api.add_resource(IndexPage, '/')
api.add_resource(CheckTaskQueue, '/tasks')
api.add_resource(BetterGetCoefs, '/get_coefs')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=True)
