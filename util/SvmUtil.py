# -*- coding: utf-8 -*-
import datetime
import os
import time

import joblib
import numpy as np
import tushare as ts
from sklearn import svm


class SvmUtil(object):

    def __init__(self):
        self.pro = ts.pro_api('2b9929516221569516ff57324dc130c6100a76fa66d4202de854ba58')

    '''
    本策略选取了七个特征变量组成了滑动窗口长度为15天的训练集,随后训练了一个二分类(上涨/下跌)的支持向量机模型.
    若没有仓位则在每个星期一的时候输入标的股票近15个交易日的特征变量进行预测,并在预测结果为上涨的时候购买标的.
    若已经持有仓位则在盈利大于10%的时候止盈,在星期五损失大于2%的时候止损.
    特征变量为:1.收盘价/均值2.现量/均量3.最高价/均价4.最低价/均价5.现量6.区间收益率7.区间标准差
    训练数据为:SHSE.600009上海机场,时间从2016-04-01到2017-07-30
    回测时间为:2017-08-01 09:00:00到2017-09-05 09:00:00
    '''

    def svm_learning(self, stockCode):
        end_time = time.strftime('%Y%m%d', time.localtime(time.time()))
        start_year = int(time.strftime('%Y', time.localtime(time.time()))) - 2
        month_day = time.strftime('%m%d', time.localtime(time.time()))
        start_time = '{}{}'.format(start_year, month_day)
        # 获取数据
        df = self.pro.daily(ts_code=stockCode, start_date=start_time, end_date=end_time)

        if df.empty:
            return None

        if len(df) < 200:
            return None

        days_value = df['trade_date'].values[::-1]
        days_close = df['close'].values[::-1]
        days = []
        # 获取行情日期列表
        for i in range(len(days_value)):
            days.append(str(days_value[i]))

        x_all = []
        day_all = []
        week_all = []
        month_all = []
        for index in range(200, len(days)):
            start_day = days[index - 200]
            end_day = days[index]
            data = self.pro.daily(ts_code=stockCode, start_date=start_day, end_date=end_day)
            open = data['open'].values[::-1]
            close = data['close'].values[::-1]
            max_x = data['high'].values[::-1]
            min_n = data['low'].values[::-1]
            amount = data['amount'].values[::-1]
            volume = []
            for i in range(len(close)):
                volume_temp = amount[i] / close[i]
                volume.append(volume_temp)

            open_mean = open[-1] / np.mean(open)  # 开盘价/均值
            close_mean = close[-1] / np.mean(close)  # 收盘价/均值
            diff_close_open_mean = close_mean - open_mean  # 收盘价均值-开盘价均值
            volume_mean = volume[-1] / np.mean(volume)  # 现量/均量
            max_mean = max_x[-1] / np.mean(max_x)  # 最高价/均价
            min_mean = min_n[-1] / np.mean(min_n)  # 最低价/均价
            diff_max_min_mean = max_mean - min_mean  # 最高价均值-最低价均值
            vol = volume[-1]  # min_mean
            return_now = close[-1] / close[0]  # 区间收益率
            std = np.std(np.array(close), axis=0)  # 区间标准差

            # 将计算出的指标添加到训练集X
            # features用于存放因子
            # features = [close_mean, volume_mean, max_mean, min_mean, vol, return_now, std]
            features = [open_mean, close_mean, diff_close_open_mean, volume_mean, max_mean, min_mean, diff_max_min_mean,
                        vol, return_now, std]
            x_all.append(features)

        for i in range(len(days_close) - 200):
            if days_close[i + 1] > days_close[i]:
                label = 1
            else:
                label = 0
            day_all.append(label)

        for i in range(len(days_close) - 200):
            if days_close[i + 5] > days_close[i]:
                label = 1
            else:
                label = 0
            week_all.append(label)

        for i in range(len(days_close) - 200):
            if days_close[i + 20] > days_close[i]:
                label = 1
            else:
                label = 0
            month_all.append(label)

        x_train = x_all[: -1]
        day_train = day_all[: -1]
        week_train = week_all[: -1]
        month_train = month_all[: -1]

        day_model = svm.SVC(C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False,
                            tol=0.001, cache_size=400, verbose=False, max_iter=-1,
                            decision_function_shape='ovr', random_state=None)
        day_model.fit(x_train, day_train)

        week_model = svm.SVC(C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False,
                             tol=0.001, cache_size=400, verbose=False, max_iter=-1,
                             decision_function_shape='ovr', random_state=None)
        week_model.fit(x_train, week_train)

        month_model = svm.SVC(C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False,
                              tol=0.001, cache_size=400, verbose=False, max_iter=-1,
                              decision_function_shape='ovr', random_state=None)
        month_model.fit(x_train, month_train)

        joblib.dump(day_model, stockCode[:-3] + "_day_model.m")
        joblib.dump(week_model, stockCode[:-3] + "_week_model.m")
        joblib.dump(month_model, stockCode[:-3] + "_month_model.m")
        return 'success'

    def svm_predict(self, stockCode):
        if not (os.path.exists(stockCode[:-3] + "_day_model.m")):
            learnResult = self.svm_learning(stockCode)
            if learnResult is None:
                return None
        today = datetime.date.today()
        first = today.replace(day=1)
        last_month = first - datetime.timedelta(days=30)
        start_time = last_month.strftime("%Y%m%d")
        end_time = time.strftime('%Y%m%d', time.localtime(time.time()))
        df = self.pro.daily(ts_code=stockCode, start_date=start_time, end_date=end_time)

        if df.empty:
            return None

        open = df['open'].values[::-1]
        close = df['close'].values[::-1]
        train_max_x = df['high'].values[::-1]
        train_min_n = df['low'].values[::-1]
        train_amount = df['amount'].values[::-1]
        volume = []
        for i in range(len(close)):
            volume_temp = train_amount[i] / close[i]
            volume.append(volume_temp)

        open_mean = open[-1] / np.mean(open)
        close_mean = close[-1] / np.mean(close)
        diff_close_open_mean = close_mean - open_mean
        volume_mean = volume[-1] / np.mean(volume)
        max_mean = train_max_x[-1] / np.mean(train_max_x)
        min_mean = train_min_n[-1] / np.mean(train_min_n)
        diff_max_min_mean = max_mean - min_mean
        vol = volume[-1]
        return_now = close[-1] / close[0]
        std = np.std(np.array(close), axis=0)

        # 得到本次输入模型的因子
        # features = [close_mean, volume_mean, max_mean, min_mean, vol, return_now, std]
        features = [open_mean, close_mean, diff_close_open_mean, volume_mean, max_mean, min_mean, diff_max_min_mean,
                    vol, return_now, std]
        features = np.array(features).reshape(1, -1)
        day_model = joblib.load(stockCode[:-3] + "_day_model.m")
        week_model = joblib.load(stockCode[:-3] + "_week_model.m")
        month_model = joblib.load(stockCode[:-3] + "_month_model.m")

        day_prediction = day_model.predict(features)[0]
        week_prediction = week_model.predict(features)[0]
        month_prediction = month_model.predict(features)[0]

        prediction = [day_prediction, week_prediction, month_prediction]

        return prediction

    @classmethod
    def svm_delete(cls):
        fileList = os.listdir()
        for fileName in fileList:
            if os.path.splitext(fileName)[1] == '.m':
                os.remove(fileName)


if __name__ == '__main__':
    code = '603088.SH'
    # SvmUtil().svm_learning(code)
    SvmUtil().svm_predict(code)
