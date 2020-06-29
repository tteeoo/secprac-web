import os
import json

contents = {}
files = os.listdir('./web/scripts')

if os.path.isfile('./web/json/vulns.json'):
    print('web/json/vulns.json already exists')
    exit()

if not os.path.isdir('./web/scripts'):
    print('cannot find web/scripts/')
    exit()

if files == []:
    print('web/scripts/ is empty')
    exit()

for file in files:
    name = file.replace('.sh', '')
    contents[name] = {
        'shell': '/bin/bash',
        'url': '/{}'.format(file),
        'points': 2,
        'name': name
    }

if not os.path.isdir('./web/json'):
    os.mkdir('./web/json')

with open('./web/json/vulns.json', 'w') as e:
    json.dump(contents, e)
