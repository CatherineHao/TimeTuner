'''
Description: 
Author: Qing Shi
Date: 2022-11-20 19:14:42
LastEditTime: 2023-07-01 22:49:36
'''
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import pandas as pd
from utils import fft_periods, dataset_information, return_all_smoothed, overview_performance, predictions_info

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
    return "hello VUE"

global gl_file_name

@app.route('/api/test/upload/', methods=['POST'])
def upload():
    file_path = '{}/data/profile_data.json'.format(FILE_ABS_PATH)
    params = request.json
    file_name = "Sunspots"
    print(params)
    if (params['filename'] != "Sunspots.csv"):
        file_name = 'Pm2.5'
    res_data = read_json(file_path)
    return jsonify(res_data[file_name])

@app.route('/api/test/fetch/', methods=["POST"])
def fetchData():
    params = request.json
    file_name = "Sunspots"
    file_select = 'sunspots'
    select_attr = 'RAW'
    if (params['filename'] != "Sunspots.csv"):
        file_name = 'Pm25'
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
    
@app.route('api/text/profile/', methods = ['POST'])
def DatasetProfile():
    # the file path is passed in the request body
    file_path = '{}/rawdata/{}'.format(FILE_ABS_PATH)                                         
    dataset_info = dataset_information(file_path)
    return jsonify(dataset_info)

@app.route('api/text/freshdata/', methods = ['POST'])
def FreshData():
    file_path = '{}/rawdata/'.format(FILE_ABS_PATH) 
    file_name = os.listdir(file_path)
    model_path = '/model/{}.m5'.format(file_name)
    smooth_data = return_all_smoothed(file_path, fft_periods)
    overview_profile = overview_performance(file_path)
    prediction_result = predictions_info(file_path, model_path, fft_periods, file_name)
    return jsonify({
                "model_result": overview_profile,
                "temporal_data": smooth_data,
                "result_data": prediction_result
                })

if __name__ == '__main__':
    app.run(debug=True)
    

