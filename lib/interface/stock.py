from flask import Flask

server = Flask(__name__)


@server.route('/test')
def index():
    return 'hello flask'
