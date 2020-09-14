import os

from selenium import webdriver

from client.miner import Mainer
from task_management.task_queue import TaskQueue

queue = TaskQueue()
miner = Mainer(queue)

result = miner.get_games(True, 'https://1xstavka.ru/en/line/Football/118593-UEFA-Europa-League/')

print(result)

