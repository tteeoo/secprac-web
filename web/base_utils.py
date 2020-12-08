import json
import os
import random

path = path = os.path.dirname(os.path.abspath(__file__))

#json functions
def checkjson(name):
    name  = '{}.json'.format(name)
    if 'json' not in os.listdir(path):
        os.mkdir(os.path.join(path, 'json'))
    if name not in os.listdir(os.path.join(path, 'json')):
        with open(os.path.join(path, 'json', name), 'w') as e:
            json.dump({}, e)

def readjson(file):
    with open(file, 'r') as e:
        return json.load(e)

def writejson(file, data):
    with open(file, 'w') as e:
        json.dump(data, e)

def gen_id(teams):
    if teams == {}:
        return '1000'
    nums = [int(teams[t]['id']) for t in teams]
    return str(int(max(nums)) + 1)


#errors for API
class ApiError(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
    
