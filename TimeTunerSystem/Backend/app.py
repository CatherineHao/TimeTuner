'''
Description: 
Author: Qing Shi
Date: 2022-11-20 19:14:42
LastEditTime: 2023-01-08 15:34:27
'''
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

FILE_ABS_PATH = os.path.dirname(__file__)

app = Flask(__name__)
CORS(app)

@app.route('/api/test/hello/', methods=['POST'])
def hello_resp():
    params = request.json
    # msg = int(params['msg'])
    # print(msg)
    return "hello VUE"

# @app.route('/api/test/hello/', methods=['GET'])
