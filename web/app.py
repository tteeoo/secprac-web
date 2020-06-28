from flask import Flask, request
import os
try:
    from .base_utils import readjson, checkjson, writejson
except: 
    from base_utils import readjson, checkjson, writejson

app = Flask(__name__)
path = os.path.dirname(os.path.abspath(__file__))

#api
@app.route('/api/team/create')
def create_team():
    if request.method != 'POST':
        return {'error': {'status': 405, 'message': 'method not allowed'}}

if __name__=='__main__':
    app.run(debug=True)