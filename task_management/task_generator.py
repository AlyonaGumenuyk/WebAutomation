from task_management.task import Task


class TaskGenerator:
    @classmethod
    def get_tournaments_gen(cls, sport_name):
        return Task('get_tournaments', [sport_name])

    @classmethod
    def get_games_gen(cls, tournament_url):
        return Task('get_games', [tournament_url])

    @classmethod
    def watch_gen(cls, game_url):
        return Task('watch', [game_url])
