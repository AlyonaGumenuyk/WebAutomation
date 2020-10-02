import json
from jsondiff import diff

json1 = json.dumps('"Asian Handicap": "Handiсap авы Ordabasy"', ensure_ascii=False)
json2 = json.dumps('"Asian Handicap": "Handicap Ordabasy"')

changes = json.loads(diff(json2, json1, load=True, dump=True))
# print(time_to_create_task.strftime('%y-%m-%d %H:%M'))
#print(changes)
print(json.loads(json1))
print(json.loads(json2))
