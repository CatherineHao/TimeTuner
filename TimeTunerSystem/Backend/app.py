'''
Description: 
Author: Qing Shi
Date: 2022-11-20 19:14:42
LastEditTime: 2023-06-29 15:05:37
'''
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

FILE_ABS_PATH = os.path.dirname(__file__)

app = Flask(__name__)
CORS(app)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

FILE_ABS_PATH = os.path.dirname(__file__)

def read_json(add):
    with open(add, 'rt', encoding="utf-8") as f:
        cr = json.load(f)
    f.close()
    return cr

@app.route('/api/test/hello/', methods=['POST'])
def hello_resp():
    params = request.json
    # msg = int(params['msg'])
    # print(msg)
    return "hello VUE"

# @app.route('/api/test/hello/', methods=['GET'])
@app.route('/api/test/upload/', methods=['GET', 'POST'])
def upload():
    file_path = '{}/data/profile_data.json'.format(FILE_ABS_PATH)
    params = request.json
    # print(params[0])
    file_name = "Sunspots"
    if (params != "Sunspots.csv"):
        file_name = 'Pm'
    res_data = read_json(file_path)
    return jsonify(res_data[file_name])

if __name__ == '__main__':
    
    app.run(debug=True)
    