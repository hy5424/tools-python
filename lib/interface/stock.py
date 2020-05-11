from flask import Flask

server = Flask(__name__)


@server.route('/ptools/test')
def index():
    return 'hello flask'
