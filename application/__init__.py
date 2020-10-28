from flask import Flask
from flask_restful import Api
from application.bigcorp.routes import bigcorp
from application.settings import SECRET_KEY

app = Flask('app')
app.register_blueprint(bigcorp)
app.secret_key = SECRET_KEY
api = Api(app)
