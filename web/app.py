from flask import Flask, request
import os
try:
    from .base_utils import readjson, checkjson, writejson
except: 
    from base_utils import readjson, checkjson, writejson, errors

app = Flask(__name__)
path = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return {'message': 'yo'}
#api
@app.route('/api/team/create')
def create_team():
    if request.method != 'POST':
        return errors.bad_method
    

if __name__=='__main__':
    app.run(debug=True)