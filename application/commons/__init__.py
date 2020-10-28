from flask import json, jsonify
import os
from application.settings import APP_STATIC


def buildResponseError(status, err):
    return jsonify({'status': status, 'error': err})


def buildResponseSuccess(service, msg):
    return jsonify({'status': 200, service: msg})


def read_static_file(file_path):
    with open(os.path.join(APP_STATIC, 'data', file_path + '.json')) as file:
        return json.load(file)
