import json
import datetime


params = json.loads('["2020-10-04 16:15:00", "Belgium. Jupiler League", "R. Charleroi", "Standard Liege"]')
print(params[0])

dt = datetime.datetime.strptime('2020-10-04 19:00', '%Y-%m-%d %H:%M')

if datetime.datetime.now() - dt < datetime.timedelta(minutes=90):
    print('yes')
else:
    print('no')
#print(changes)
