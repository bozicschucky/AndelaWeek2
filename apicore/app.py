from flask import Flask
from instance.config import DevelopmentConfig
from flask_restplus import Api
app = Flask(__name__, instance_relative_config=True)

app.config.from_object(DevelopmentConfig)
# app.config.from_pyfile()


api = Api(app, prefix='/api/v2', version='2.0',
          title='StackoverFlowLite', description='Q and A api')

from apicore.routes import *
