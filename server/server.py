from dataclasses import dataclass, field
from datetime import datetime
from queue import Queue

from flask import Flask, jsonify, make_response, render_template
from flask_restful import Resource, Api

from client.better import Better
from client.miner import Mainer

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
api = Api(app)


@dataclass
class Task:
    method: str
    params: list
    birth_timestamp: str = field(default_factory=lambda: datetime.now().strftime("%m/%d/%Y, %H:%M:%S:%f"))


class TaskQueue(Queue):
    def __init__(self, *args, **kwargs):
        super(TaskQueue, self).__init__(*args, **kwargs)

    def put(self, task_instance, **kwargs):
        if isinstance(task_instance, Task):
            super().put(task_instance)
        else:
            print('Not A Task')


class TaskGenerator:
    @classmethod
    def get_tournaments_gen(cls, task_queue):
        task = Task('get_tournaments', [True, 'Football'])
        task_queue.put(task)


class TaskManeger:
    def __init__(self):
        self.task_queue = TaskQueue()

    def generate_task(self):
        TaskGenerator.get_tournaments_gen(self.task_queue)

    def work(self):
        if self.task_queue.empty():
            self.generate_task()
        task = self.task_queue.get()
        if task.method == 'get_tournaments':
            mainer = Mainer(self.task_queue)
            report = mainer.get_tournaments(True, 'Football')
            mainer.driver.close()
            return report


task_manager = TaskManeger()


class IndexPage(Resource):
    @staticmethod
    def get():
        result = task_manager.work()
        return make_response(jsonify(result))


class GetTaskBetter(Resource):
    @staticmethod
    def get():
        better = Better()
        result = better.get_coefs(
            'https://1xstavka.ru/en/live/Football/1306701-Germany-Oberliga-Rheinland-Pfalz/255363145-Hassia-Bingen-SG-2000-Mulheim-Karlich/')
        return jsonify(result)


api.add_resource(IndexPage, '/')
api.add_resource(GetTaskBetter, '/get_coefs')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=True)
