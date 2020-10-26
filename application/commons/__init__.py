from flask import jsonify


def buildResponseError(status, err):
    return jsonify({'status': status, 'error': err})


def buildResponseSuccess(service, msg):
    return jsonify({'status': 200, service: msg})
