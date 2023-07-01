'''
Description: 
Author: Qing Shi
Date: 2022-11-20 19:14:42
LastEditTime: 2023-06-29 15:05:37
'''
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json
import os
import pandas as pd

FILE_ABS_PATH = os.path.dirname(__file__)

app = Flask(__name__)
CORS(app)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'timetuner'

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

global gl_file_name

# @app.route('/api/test/hello/', methods=['GET'])
@app.route('/api/test/upload/', methods=['POST'])
def upload():
    file_path = '{}/data/profile_data.json'.format(FILE_ABS_PATH)
    params = request.json
    file_name = "Sunspots"
    print(params)
    if (params['filename'] != "Sunspots.csv"):
        file_name = 'Pm2.5'
    res_data = read_json(file_path)
    # gl_file_name = file_name
    return jsonify(res_data[file_name])

@app.route('/api/test/fetch/', methods=["POST"])
def fetchData():
    # print(session)
    params = request.json
    file_name = "Sunspots"
    file_select = 'sunspots'
    # print(params)
    # session["file_name"] = file_name
    # print(session.get("file_name"))
    select_attr = 'RAW'
    if (params['filename'] != "Sunspots.csv"):
        file_name = 'Pm2.5'
        file_select = 'pm'
        select_attr = 'pm25'
    file_path = '{}/data/{}/'.format(FILE_ABS_PATH, file_name)
    model_result = read_json(file_path + 'model_results.json')
    result_data = pd.read_csv(file_path + 'result_data.csv').to_json()
    temporal_data = pd.read_csv(file_path + 'temporal_data.csv').to_json()
    return jsonify({
        "model_result": model_result,
        "result_data": result_data,
        "temporal_data": temporal_data,
        "file_name": file_select,
        "select_attr": select_attr
    })

if __name__ == '__main__':
    app.run(debug=True)
    