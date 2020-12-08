from flask import Flask, request, abort, render_template
from werkzeug.exceptions import HTTPException
from datetime import datetime
import json
import os

timef = "%Y-%m-%d %H:%M"

app = Flask(__name__, static_folder='static')
path = os.path.dirname(os.path.abspath(__file__))
if not os.path.isfile(os.path.join(path, 'config.py')):
    print('run the configure.py script first')
    exit(1)

try:
    from .base_utils import readjson, checkjson, writejson, gen_id, ApiError
    from .config import name
except ImportError:
    from base_utils import readjson, checkjson, writejson, gen_id, ApiError
    from config import name

teams_file = os.path.join(path, 'json', 'teams.json')
vulns_file = os.path.join(path, 'json', 'vulns.json')
checkjson('vulns')
jvulns = readjson(vulns_file)
if jvulns == {} or jvulns == []:
    print('please enter a valid vulns.json file')
    exit(1)

total_points = 0
for script in jvulns:
    total_points += jvulns[script]['points']

debug = False
if __name__ == '__main__':
    debug = True

# frontend web interface endpoints

# home page
@app.route('/')
def home():
    return render_template('index.html', points=total_points, name=name)

# about page
@app.route('/about')
def about():
    return render_template('about.html')


# api endpoints

# endpoint to create new team
@app.route('/api/team/create', methods=['post'])
def create_team():
    try:
        data = json.loads(request.data.decode('utf-8'))
    except:
        raise ApiError('bad json', 400)
    checkjson('teams')

    token = data['token']
    teams = readjson(teams_file)
    vs = {i: False for i in jvulns}
    time = datetime.strftime(datetime.now(), timef)
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

# endpoint for team done
@app.route('/api/team/done', methods=['post'])
def team_done():
    try:
        data = json.loads(request.data.decode('utf-8'))
    except:
        raise ApiError('bad json', 400)

    if 'token' not in data: raise ApiError('no token provided', 401)

    token = data['token']
    teams = readjson(teams_file)
    if token not in teams: raise ApiError('invalid token', 401)

    team = teams[token]
    vulns = team['vulns']
    for v in vulns:
        if not vulns[v]:
            raise ApiError('team not completed', 400)

    return {'completed': True}

# endpoint to return the vulns.json file
@app.route('/api/vuln/vulns.json', methods=['get'])
def vulns_f():
    token = request.headers.get('token')
    checkjson('teams')
    t = readjson(teams_file)
    if token:
        if token in t:
            return jvulns
        raise ApiError('invalid token', 401)
    raise ApiError('no token provided', 401)

# endpoint to set vuln as completed
@app.route('/api/vuln/done', methods=['post'])
def done():
    try:
        data = json.loads(request.data.decode('utf-8'))
    except:
        raise ApiError('bad json', 400)

    checkjson('teams')
    teams = readjson(teams_file)

    if 'token' not in data: raise ApiError('no token provided', 401)
    if 'name' not in data: raise ApiError('no name provided', 401)
    token, name, time = data['token'], data['name'], datetime.strftime(datetime.now(), timef)

    if token not in teams: raise ApiError('invalid token', 401)
    if name not in teams[token]['vulns']: raise ApiError('invalid vuln name', 400)
    if teams[token]['vulns'][name]: raise ApiError('already solved', 400)

    teams[token]['vulns'][name] = True
    points = jvulns[name]['points']
    new_points = teams[token]['points'] + points
    teams[token]['points'] = new_points
    teams[token]['times'][time] = {
        'points': new_points
    }

    writejson(teams_file, teams)

    return {'awarded': points}

# endpoint for when vuln fix is undone
@app.route('/api/vuln/undo', methods=['post'])
def undo():
    try:
        data = json.loads(request.data.decode('utf-8'))
    except:
        raise ApiError('bad json', 400)

    checkjson('teams')
    teams = readjson(teams_file)

    if 'token' not in data: raise ApiError('no token provided', 401)
    if 'name' not in data: raise ApiError('no name provided', 401)
    token, name, time = data['token'], data['name'], datetime.strftime(datetime.now(), timef)

    if token not in teams: raise ApiError('invalid token', 401)
    if name not in teams[token]['vulns']: raise ApiError('invalid vuln name', 400)
    if not teams[token]['vulns'][name]: raise ApiError('not solved', 400)

    teams[token]['vulns'][name] = False
    points = 0 - jvulns[name]['points']
    new_points = teams[token]['points'] + points
    teams[token]['points'] = new_points
    teams[token]['times'][time] = {
        'points': new_points
    }

    writejson(teams_file, teams)

    return {'awarded': points}

# endpoint to download scripts
@app.route('/api/scripts/<name>')
def download_script(name):
    if name not in os.listdir(os.path.join(path, 'scripts')):
        abort(404)
    token = request.headers.get('token')
    checkjson('teams')
    t = readjson(teams_file)
    token = request.headers.get('token')
    if token:
        if token in t:
            if '..' in name:
                raise ApiError('relative paths not allowed')
            f = open(os.path.join(path, 'scripts', name), 'r')
            c = f.read()
            return c
        raise ApiError('invalid token', 401)
    raise ApiError('no token provided', 401)

# endpoint to download setup scripts
@app.route('/api/scripts/setup/<name>')
def download_setup_script(name):
    if name not in os.listdir(os.path.join(path, 'scripts', 'setup')):
        abort(404)
    checkjson('teams')
    t = readjson(teams_file)
    token = request.headers.get('token')
    if token:
        if token in t:
            if '..' in name:
                raise ApiError('relative paths not allowed')
            f = open(os.path.join(path, 'scripts', 'setup', name), 'r')
            c = f.read()
            return c
        raise ApiError('invalid token', 401)
    raise ApiError('no token provided', 401)


# endpoint to get info for one team
@app.route('/api/public/team/<name>', methods=['get'])
def get_team(name):
    checkjson('teams')
    id_teams = {}
    teams = readjson(teams_file)

    for k in teams:
        id_teams[teams[k]['id']] = {}
        id_teams[teams[k]['id']]['points'] = teams[k]['points']
        try:
            id_teams[teams[k]['id']]['times'] = teams[k]['times']
        except KeyError:
            id_teams['times'] = {}

    if name not in id_teams: raise ApiError('invalid team', 400)

    return id_teams[name]

# endpoint to get leaderboard
@app.route('/api/public/leaderboard/<per>/<page>')
def leaderboard(per, page):
    per = int(per)
    page = int(page) - 1

    checkjson('teams')
    json_teams = readjson(teams_file)


    teams = []
    for team in json_teams:
        times = []
        for t in json_teams[team]['times'].keys():
            times.append(datetime.fromisoformat(t))
        teams.append({
            'id': json_teams[team]['id'],
            'points': json_teams[team]['points'],
            'start': datetime.strftime(sorted(times)[0], timef)
        })
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

    try:
        pages[page]
    except KeyError:
        raise ApiError('page does not exist', 400)

    data = {}
    for team in range(len(pages[page])):
        data[page * per + team + 1] = pages[page][team]

    return {'board': data, 'pages': page_count, 'teams': len(teams)}

# errors
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

        return {'error': {'message': name, 'status': code}}

# api errors
@app.errorhandler(ApiError)
def api_e(e):
    return {'error': {'status': e.code, 'message': e.message}}, e.code

if __name__=='__main__':
    app.run(debug=debug, host='0.0.0.0')
