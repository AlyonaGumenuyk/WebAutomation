import datetime


time_to_create_task = datetime.datetime.now() - datetime.timedelta(minutes=1)
print(time_to_create_task.strftime('%y-%m-%d %H:%M'))
