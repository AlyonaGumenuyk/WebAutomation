from task_management.task import Task


class TaskGenerator:
    @classmethod
    def get_tournaments_gen(cls, task_queue):
        task = Task('get_tournaments', ['Squash'])
        task_queue.put(task)

    @classmethod
    def get_games_gen(cls, task_queue, tournament_url):
        task = Task('get_games', [tournament_url])
        task_queue.put(task)

    @classmethod
    def watch_gen(cls, task_queue, game_url):
        task = Task('watch', [game_url])
        task_queue.put(task)
