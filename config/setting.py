# -*- coding: utf-8 -*-
import os
import sys


class Config(object):
    DEBUG = False

    def __getitem__(self, item):
        return self.__getattribute__(item)


class DevelopmentConfig:
    SERVER_PORT = 8093
    STOCK_SOURCE = "sina"  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
    DB_CONFIG = "mysql+pymysql://root:123456@172.18.0.100:3306/TOOLS?charset=utf8mb4"


class ProductionConfig:
    SERVER_PORT = 8093
    STOCK_SOURCE = "sina"  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
    DB_CONFIG = "mysql+pymysql://root:root@172.17.176.183:3306/TOOLS?charset=utf8mb4"


mapping = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig
}

num = len(sys.argv) - 1
if num < 1 or num > 1:
    exit("参数错误,必须传环境变量!比如: python xx.py dev|pro|default")

env = sys.argv[1]
APP_ENV = os.environ.get('APP_ENV', env).lower()
config = mapping[APP_ENV]()
