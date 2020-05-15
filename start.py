# -*- coding: utf-8 -*-
from config.setting import config as conf
from lib.interface.stock import server

server.run(port=conf.SERVER_PORT, host='0.0.0.0')
