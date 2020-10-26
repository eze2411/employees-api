from flask import Flask, json, session
from flask_restful import Api
import os
from application.bigcorp.routes import bigcorp
from application.settings import APP_STATIC

app = Flask('app')
app.register_blueprint(bigcorp)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
api = Api(app)


def buildDataObjects():
    with open(os.path.join(APP_STATIC, 'data', 'departments.json')) as file:
        departments = {}
        for item in json.load(file):
            departments.update({str(item.get('id')): item})
        session['departments'] = departments
    with open(os.path.join(APP_STATIC, 'data', 'offices.json')) as file:
        offices = {}
        for item in json.load(file):
            offices.update({str(item.get('id')): item})
        session['offices'] = offices
    pass


app.before_first_request(buildDataObjects)
