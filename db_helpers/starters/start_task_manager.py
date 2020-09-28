import json

from db_helpers.task_manager import TaskManager

task_manager = TaskManager()
#records = task_manager.get_all_tasks('miner')
#records = task_manager.get_task_for_execution('miner')
#task_manager.change_task_state('completed', 1)
task_manager.add_result(dict({'result': 'some result', 'task_id': 1, 'method': 'games'}))
#print(json.loads(records))
