from flask import Flask
from instance.config import DevelopmentConfig
from flask_restplus import Api
from flask_jwt_extended import JWTManager


app = Flask(__name__, instance_relative_config=True)

app.config.from_object(DevelopmentConfig)
app.config['RESTPLUS_VALIDATE'] = True
app.config['JWT_SECRET_KEY'] = 'random#$8990000000secret'
# swagger ui configs
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
app.config.SWAGGER_UI_OPERATION_ID = True
app.config.SWAGGER_UI_REQUEST_DURATION = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False


jwt = JWTManager(app)

api = Api(app, prefix='/api/v2', version='2.0',
          title='StackoverFlowLite', description='Q and A api')

from apicore.routes import *
