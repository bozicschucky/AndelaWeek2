from flask import Flask
from instance.config import DevelopmentConfig
app = Flask(__name__, instance_relative_config=True)

app.config.from_object(DevelopmentConfig)
# app.config.from_pyfile()


@app.route('/')
def hello_world():
    return 'Hello, World!'
