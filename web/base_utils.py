import json
import os

path = path = os.path.dirname(os.path.abspath(__file__))

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

class errors:
    bad_method = {'error': {'status': 405, 'message': 'method not allowed'}}
    not_found = {'error': {'status': 404, 'message': 'not found'}}
    bad_json = {'error': {'status': 400, 'message': 'bad json'}}
    