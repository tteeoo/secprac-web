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

#endpoint for team done
@app.route('/api/team/done', methods=['post'])
def team_done():
    try:
        data = json.loads(request.data.decode('utf-8'))
    except:
        raise ApiError('bad json', 400)
    if 'token' not in data:
        raise ApiError('no token provided', 401)
    token = data['token']
    teams = readjson(teams_file)
    if token not in teams:
        raise ApiError('invalid token', 401)
    team = teams[token]
    vulns = team['vulns']
    for v in vulns:
        if not vulns[v]:
            raise ApiError('team not completed', 400)
    return {'completed': True}

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
    writejson(teams_file, teams)
    return {'awarded': points}

#endpoint for when vuln fix is undone
@app.route('/api/vuln/undo', methods=['post'])
def undo():
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
    if not teams[token]['vulns'][name]:
        raise ApiError('not solved', 400)
    teams[token]['vulns'][name] = False
    vulns = readjson(vulns_file)
    points = 0 - vulns[name]['points']
    new_points = teams[token]['points'] + points
    teams[token]['points'] = new_points
    teams[token]['times'][time] = {
        'points': new_points
    }
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

#endpoint to download setup scripts
@app.route('/api/scripts/setup/<name>')
def download_setup_script(name):
    if name not in os.listdir('./scripts/setup'):
        abort(404)
    token = request.headers.get('token')
    checkjson('teams')
    t = readjson(teams_file)
    if token:
        if token in t:
            f = open('scripts/setup/{}'.format(name), 'r')
            c = f.read()
            return c
        raise ApiError('invalid token', 401)
    raise ApiError('no token provided', 401)


#endpoint to get info for one team
@app.route('/api/public/team/<name>', methods=['get'])
def get_team(name):
    checkjson('teams')
    teams = readjson(teams_file)
    if name not in teams:
        raise ApiError('invalid token', 401)
    return teams[name]

#endpoint to get leaderboard
@app.route('/api/public/leaderboard/<per>/<page>')
def leaderboard(per, page):
    per = int(per)
    page = int(page) - 1
    checkjson('teams')
    json_teams = readjson(teams_file)
    teams = []
    for team in json_teams:
        teams.append({'id': json_teams[team]['id'], 'points': json_teams[team]['points']})
    teams = sorted(teams, key=lambda k: k['points'], reverse=True)
    page_count = 0
    if len(teams) % per != 0:
        page_count = round(len(teams) / per)
        if page_count < len(teams) / 7:
            page_count += 1
    else:
        page_count = round(len(teams) / per)
    pages = {}
    for i in range(page_count):
        upper = i * per + per
        if upper > len(teams):
            upper = len(teams)
        pages[i] = teams[i * per:upper]
    data = {}
    try:
        pages[page]
    except KeyError:
        raise ApiError('page does not exist', 400)
    for team in range(len(pages[page])):
        data[page * per + team + 1] = pages[page][team]
    return data

#errors
if not debug:
    @app.errorhandler(Exception)
    def error(e):
        code = 500
        name = "Internal Server Error"
        if isinstance(e, HTTPException):
            code = e.code
            name = e.name
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
