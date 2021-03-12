# -*- coding: utf-8 -*-
import easyquotation
from flask import Flask, request

from config.setting import config as conf
from util.AverageStockSelectionUtil import AverageStockSelectionUtil
from util.GetStockPrice import GetStockPrice
from util.LotteryUtil import LotteryUtil
from util.SvmUtil import SvmUtil

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


@server.route('/ptools/getStockSvmLearning', methods=['POST'])
def getStockSvmLearning():
    stockCode = request.json['stockCode']
    svm = SvmUtil()
    svm.svm_learning(stockCode)
    return 'success'


@server.route('/ptools/getStockSvmResult', methods=['POST'])
def getStockSvm():
    stockCode = request.json['stockCode']
    svm = SvmUtil()
    prediction = svm.svm_predict(stockCode)
    return str(prediction)


@server.route('/ptools/getStockMASvmResult', methods=['POST'])
def getStockMASvm():
    stockCode = request.json['stockCode']
    avg_svm = AverageStockSelectionUtil()
    avg_prediction = avg_svm.svm_predict(stockCode)
    return str(avg_prediction)


@server.route('/ptools/deleteStockModel', methods=['POST'])
def deleteModel():
    svm = SvmUtil()
    svm.svm_delete()
    return 'success'


@server.route('/ptools/getLottery', methods=['POST'])
def getLottery():
    lottery = LotteryUtil()
    result = lottery.random_ball()
    return str(result)


@server.route('/ptools/getStockPrice', methods=['POST'])
def getStockPrice():
    stockCode = request.json['stockCode']
    days = request.json['days']
    get_price = GetStockPrice()
    data = get_price.get_price(stockCode, days)
    return str(data)
