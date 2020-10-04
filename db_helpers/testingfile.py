import json
import datetime




dt = datetime.datetime.strptime('2020-10-04 22:08:00', '%Y-%m-%d %H:%M:%S')

if datetime.datetime.now() - dt < datetime.timedelta(minutes=90):
    print('yes')
else:
    print('no')
#print(changes)
