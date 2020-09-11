from client.better import Better

# class TaskQueue(Queue):
#
#
#
# class Worker():
#     def __init__(self, **init_params):
#         self.task_queue = TaskQueue()
#         self.dr 'https://1xstavka.ru/en/line/Football/118587-UEFA-Champions-League/'iver = webdriver.chrome

# mainer = Mainer()
better = Better()
try:
    # print(mainer.get_games(True, "https://1xstavka.ru/en/line/Football/1706694-UEFA-Nations-League/"))
    # better.login("mrwithoutnickname@gmail.com", "h6E-qYg-FDR-7b8")
    print(better.get_coefs(
        'https://1xstavka.ru/en/live/Football/1306701-Germany-Oberliga-Rheinland-Pfalz/255363145-Hassia-Bingen-SG-2000-Mulheim-Karlich/'))
finally:
    # mainer.driver.close()
    better.driver.close()
