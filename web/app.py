from flask import Flask, request
from werkzeug.exceptions import HTTPException
import os
import json
try:
    from .base_utils import readjson, checkjson, writejson, errors, gen_id
except: 
    from base_utils import readjson, checkjson, writejson, errors, gen_id

app = Flask(__name__)
path = os.path.dirname(os.path.abspath(__file__))
teams_file = os.path.join(path, 'json', 'teams.json')
if __name__=='__main__':
    debug=True

@app.route('/')
def home():
    return {'message': 'yo'}
#api
@app.route('/api/team/create', methods=['post'])
def create_team():
    try:
        data = json.loads(request.data.decode('utf-8'))
    except:
        return errors.bad_json
    checkjson('teams')
    token = data['Token']
    teams = readjson(teams_file)
    tid = gen_id(teams)
    if token not in teams:
        team = {
            'id': tid,
            'ip': request.remote_addr,
            'token': token,
            'points': 0
        }
        teams[token] = team
        writejson(teams_file, teams)
        return {'ID': tid}
    return {'ID': teams[token]['id']}

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

if __name__=='__main__':
    app.run(debug=debug, host='0.0.0.0')