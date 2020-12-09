#!/usr/bin/env python3
import os
import sys
import json

# get the team name
cname = '' 
if len(sys.argv) < 2:
    print('run again like this:\n\n{} "<name of this challenge>"\n\nnotice the double quotes (needed if you use any spaces)'.format(sys.argv[0]))
    exit(1)
cname = sys.argv[1]

contents = {}
files = os.listdir('./web/scripts')

# ask before overwriting json file
if os.path.isfile('./web/json/vulns.json'):
    answer = ''
    while answer != 'n' and answer != 'y':
        answer = input('web/json/vulns.json already exists, overwrite? (y/n): ')
    if answer == 'n':
        exit(1)

# ensure scripts directory exists before proceeding
if not os.path.isdir('./web/scripts'):
    print('cannot find web/scripts/')
    exit(1)

# get names of script files
if files == []:
    print('web/scripts/ is empty')
    exit(1)

# iterate script filenames
for file in files:

    # read file
    try:
        f = open('./web/scripts/' + file, 'r')
    except IsADirectoryError:
        continue
    data = f.readlines()
    f.close()

    # default values
    shell = '/bin/bash'
    name = file.split('.')[0]
    points = 2
    setup = ''

    # get shell
    try:
        if data[0][0] + data[0][1] == '#!':
            shell = data[0][2:len(data[0])-1]
    except IndexError:
        pass

    # get name
    try:
        if data[1][0] == '#':
            if data[1][1] == ' ':
                name = data[1][2:]
            else:
                name = data[1][1:]
            split = name.split(' ')
            name = ' '.join(split[:len(split)-1])
            
            # get points
            try:
                points = int(split[-1])
            except TypeError:
                pass
    except IndexError:
        pass

    # get setup
    try:
        if data[2][0] == '#':
            if data[2][1] == ' ':
                setup = data[2][2:]
            else:
                setup = data[2][1:]
            split = setup.split(' ')
            setup = ' '.join(split)
            setup = setup[:len(setup)-1]
    except IndexError:
        pass

    # set data
    contents[name] = {
        'shell': shell,
        'url': '{}'.format(file),
        'points': points,
        'setup_url': setup,
        'name': name
    }

# make json directory if it does not exist
if not os.path.isdir('./web/json'):
    os.mkdir('./web/json')

# write data
with open('./web/json/vulns.json', 'w') as e:
    json.dump(contents, e)
with open('./web/config.py', 'w') as e:
    e.write('game_name = "{}"'.format(cname))
