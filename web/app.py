from flask import Flask, request
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
            }
        }
        teams[token] = team
        writejson(teams_file, teams)
        return {'id': tid}
    raise ApiError('team already registered', 400)

#endpoint to return the vulns.json file
@app.route('/api/vulns.json')
def vulns_f():
    if request.headers.get('token'):
        file = readjson(vulns_file)
        return json.dumps(file)
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
            return {'error': {'message': name, 'status': code}}
        #change when error pages
        return {'error': {'message': name, 'status': code}}

#api errors
@app.errorhandler(ApiError)
def api_e(e):
    return {'error': {'status': e.code, 'message': e.message}}, e.code

if __name__=='__main__':
    app.run(debug=debug, host='0.0.0.0')
