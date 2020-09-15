import os

from selenium import webdriver

from client.better import Better
from client.miner import Mainer
from task_management.task_queue import TaskQueue

queue = TaskQueue()
#miner = Mainer(queue)
better = Better(queue)

#result = miner.get_games(True, 'https://1xstavka.ru/en/line/Football/118593-UEFA-Europa-League/')

result = better.get_coefs('https://1xstavka.ru/en/live/Football/2120110-ACL-Indoor/256326119-Atletico-Madrid-ACL-Bayern-Munich-ACL/')

print(result)

