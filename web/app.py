from flask import Flask, request
from werkzeug.exceptions import HTTPException
import os
try:
    from .base_utils import readjson, checkjson, writejson
except: 
    from base_utils import readjson, checkjson, writejson

app = Flask(__name__)
path = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return {'message': 'yo'}
#api
@app.route('/api/team/create', methods=['post'])
def create_team():
    return 'good boy'

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
    app.run(debug=True, host='0.0.0.0')