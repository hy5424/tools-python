from config.setting import SERVER_PORT
from lib.interface.stock import server

server.run(port=SERVER_PORT, host='0.0.0.0')
