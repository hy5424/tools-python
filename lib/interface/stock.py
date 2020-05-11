from flask import Flask

server = Flask(__name__, static_folder='/ptools')


@server.route('/test')
def index():
    return 'hello flask'
