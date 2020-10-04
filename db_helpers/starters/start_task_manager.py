import json

from db_helpers.task_manager import TaskManager

task_manager = TaskManager()
# records = task_manager.get_all_tasks('miner')
# records = task_manager.get_task_for_execution('miner')

# task_manager.insert_into_tasks(skill='watch', arguments=json.dumps(['date', 'Kazakhstan. Premier League',
#                                                                     'Orda\'basy', 'Taraz'],
#                                                                    ensure_ascii=False),
#                                attempts=0, worker_type='better',
#                                state='waiting for execution')


game = json.dumps([{'Date of Match': '04.10', 'Time of Match': '23:36',
                   'Tournament name': 'Portugal. Primeira Liga',
                    'Left command name': 'Portimonense', 'Right command name': 'Sporting Lisbon'}])

task_manager.add_games({'result': game})
# task_manager.insert_into_tasks(skill='watch', arguments=["2020-10-04 22:06:00", "Brazil. Campeonato Brasileiro Série D", "лево", "право"],
#                                attempts=0, worker_type='better',
#                                state=task_manager.task_init_state)

# task_manager.change_task_state('completed', 1)
# print(json.loads(records))
