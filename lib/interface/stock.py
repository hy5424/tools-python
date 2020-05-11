import flask

server = flask.Flask(__name__)


@server.route('/index')
def index():
    return 'hello flask'
