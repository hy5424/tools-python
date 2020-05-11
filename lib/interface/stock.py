from flask import Flask

server = Flask(__name__)


@server.route('/index')
def index():
    return 'hello flask'
