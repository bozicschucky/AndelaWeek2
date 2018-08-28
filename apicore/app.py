from flask import Flask
from instance.config import DevelopmentConfig
from flask_restplus import Api
from flask_jwt_extended import JWTManager


app = Flask(__name__, instance_relative_config=True)

app.config.from_object(DevelopmentConfig)
# app.config.from_pyfile()
app.config['RESTPLUS_VALIDATE'] = True
app.config['JWT_SECRET_KEY'] = 'random#$8990000000secret'


jwt = JWTManager(app)

api = Api(app, prefix='/api/v2', version='2.0',
          title='StackoverFlowLite', description='Q and A api')

from apicore.routes import *
