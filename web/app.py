from flask import Flask, request, abort
from werkzeug.exceptions import HTTPException
import os
import json
try:
    from .base_utils import readjson, checkjson, writejson, gen_id, ApiError
except: 
    from base_utils import readjson, checkjson, writejson, gen_id, ApiError

app = Flask(__name__)
path = os.path.dirname(os.path.abspath(__file__))
teams_file = os.path.join(path, 'json', 'teams.json')
vulns_file = os.path.join(path, 'json', 'vulns.json')
checkjson('vulns')
if readjson(vulns_file) == {} or readjson(vulns_file) == []:
    print('please enter a valid vulns.json file')
    exit()
debug = False
if __name__ == '__main__':
    debug = True

#frontend web interface endpoints

#home page
@app.route('/')
def home():
    return {'message': 'yo'}


#api endpoints

#endpoint to create new team
@app.route('/api/team/create', methods=['post'])
def create_team():
    try:
        data = json.loads(request.data.decode('utf-8'))
    except:
        raise ApiError('bad json', 400)
    checkjson('teams')
    token = data['token']
    teams = readjson(teams_file)
    vulns = readjson(vulns_file)
    vs = {i: False for i in vulns}
    time = data['time']
    tid = gen_id(teams)
    if token not in teams:
        team = {
            'id': tid,
            'ip': request.remote_addr,
            'token': token,
            'points': 0,
            'times': {
                time: {'points': 0}
            },
            'vulns': vs
        }
        teams[token] = team
        writejson(teams_file, teams)
        return {'id': tid}
    raise ApiError('team already registered', 400)

#endpoint to return the vulns.json file
@app.route('/api/vuln/vulns.json', methods=['get'])
def vulns_f():
    token = request.headers.get('token')
    checkjson('teams')
    t = readjson(teams_file)
    if token:
        if token in t:
            file = readjson(vulns_file)
            return json.dumps(file)
        raise ApiError('invalid token', 401)
    raise ApiError('no token provided', 401)

#endpoint to set vuln as completed
@app.route('/api/vuln/done', methods=['post'])
def done():
    try:
        data = json.loads(request.data.decode('utf-8'))
    except:
        raise ApiError('bad json', 400)
    checkjson('teams')
    teams = readjson(teams_file)
    if 'token' not in data:
        raise ApiError('no token provided', 401)
    if 'name' not in data:
        raise ApiError('no name provided', 401)
    if 'time' not in data:
        raise ApiError('no time provided', 401)
    token, name, time = data['token'], data['name'], data['time']
    if token not in teams:
        raise ApiError('invalid token', 401)
    if name not in teams[token]['vulns']:
        raise ApiError('invalid vuln name', 400)
    if teams[token]['vulns'][name]:
        raise ApiError('already solved', 400)
    teams[token]['vulns'][name] = True
    vulns = readjson(vulns_file)
    points = vulns[name]['points']
    new_points = teams[token]['points'] + points
    teams[token]['points'] = new_points
    teams[token]['times'][time] = {
        'points': new_points
    }
    print(json.dumps(teams))
    writejson(teams_file, teams)
    return {'awarded': points}

#endpoint to download scripts
@app.route('/api/scripts/<name>')
def download_script(name):
    if name not in os.listdir('./scripts'):
        abort(404)
    token = request.headers.get('token')
    checkjson('teams')
    t = readjson(teams_file)
    if token:
        if token in t:
            f = open('scripts/{}'.format(name), 'r')
            c = f.read()
            return c
        raise ApiError('invalid token', 401)
    raise ApiError('no token provided', 401)


#errors
if not debug:
    @app.errorhandler(Exception)
    def error(e):
        code = 500
        name = "Internal Server Error"
        if isinstance(e, HTTPException):
            code = e.code
            name = e.name
        print(request.path)
        if request.path.startswith('/api'):
            return {'error': {'message': name, 'status': code}}, code
        #change when error pages
        return {'error': {'message': name, 'status': code}}

#api errors
@app.errorhandler(ApiError)
def api_e(e):
    return {'error': {'status': e.code, 'message': e.message}}, e.code

if __name__=='__main__':
    app.run(debug=debug, host='0.0.0.0')
