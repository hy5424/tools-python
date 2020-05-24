# -*- coding: utf-8 -*-
import easyquotation
from flask import Flask, request

from config.setting import config as conf

server = Flask(__name__)


@server.route('/ptools/getStockList')
def stockList():
    quotation = easyquotation.use(conf.STOCK_SOURCE)  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
    stockades = quotation.market_snapshot(prefix=True)  # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀
    # dict_json = json.loads(json.dumps(stockades))
    # db = DBUtil(DB_CONFIG)
    # str = ''
    # for key in dict_json:
    #     codeStr = '{1}{0}{1}'.format(key, "'")
    #     nameStr = '{1}{0}{1}'.format(dict_json[key]['name'], "'")
    #     str += "insert into stock(code, name) value (" + codeStr + ", " + nameStr + ");"
    # db.execute_many_sql(str[:-1])
    return stockades


@server.route('/ptools/getStockByCode', methods=['POST'])
def getStockByCode():
    quotation = easyquotation.use(conf.STOCK_SOURCE)
    stockCode = request.json['stockCode']
    stockData = quotation.real(stockCode)
    return stockData
