import os
import json

contents = {}
files = os.listdir('./web/scripts')

if os.path.isfile('./web/json/vulns.json'):
    answer = ''
    while answer != 'n' and answer != 'y':
        answer = input('web/json/vulns.json already exists, overwrite? (y/n): ')
    if answer == 'n':
        exit(1)

if not os.path.isdir('./web/scripts'):
    print('cannot find web/scripts/')
    exit(1)

if files == []:
    print('web/scripts/ is empty')
    exit(1)

for file in files:
    f = open('./web/scripts/' + file, 'r')
    data = f.readlines()
    f.close()
    shell = '/bin/bash'
    name = file.split('.')[0]
    points = 2

    try:
        if data[0][0] + data[0][1] == '#!':
            shell = data[0][2:len(data[0])-1]
        if data[1][0] == '#':
            if data[1][1] == ' ':
                name = data[1][2:]
            else:
                name = data[1][1:]
            split = name.split(' ')
            try:
                points = int(split[-1])
                name = ' '.join(split[:len(split)-1])
            except TypeError:
                pass
    except IndexError:
        pass

    contents[name] = {
        'shell': shell,
        'url': '{}'.format(file),
        'points': points,
        'name': name
    }

if not os.path.isdir('./web/json'):
    os.mkdir('./web/json')

with open('./web/json/vulns.json', 'w') as e:
    json.dump(contents, e)
