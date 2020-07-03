# -*- coding: utf-8 -*-
import datetime
import time

import joblib
import numpy as np
import tushare as ts
from sklearn import svm


class AverageStockSelectionUtil(object):

    def __init__(self):
        self.pro = ts.pro_api('2b9929516221569516ff57324dc130c6100a76fa66d4202de854ba58')

    def svm_learning(self, stockCode):
        today = datetime.date.today()
        day60 = today - datetime.timedelta(days=1000)
        start_time = day60.strftime("%Y%m%d")
        end_time = time.strftime('%Y%m%d', time.localtime(time.time()))

        # 获取数据
        df = self.pro.daily(ts_code=stockCode, start_date=start_time, end_date=end_time)

        if df.empty:
            return None

        if len(df) < 500:
            return None

        close_values = df['close'].values[::-1]

        close = []
        close_y = []
        for i in range(len(close_values)):
            close.append(close_values[i])
            close_y.append(close_values[i])

        day5_close_mean = []
        day10_close_mean = []
        day20_close_mean = []

        for index in range(500):
            day5_close = []
            day10_close = []
            day20_close = []
            for i in range(len(close)):
                if i < 5:
                    day5_close.append(close[-i - 1])
                if i < 10:
                    day10_close.append(close[-i - 1])
                if i < 20:
                    day20_close.append(close[-i - 1])

            day5_close_mean.append(np.mean(day5_close))
            day10_close_mean.append(np.mean(day10_close))
            day20_close_mean.append(np.mean(day20_close))
            close.pop()

        x_all = []
        day_all = []
        week_all = []
        month_all = []
        for i in range(len(day5_close_mean)):
            if i == len(day5_close_mean) - 1:
                break
            day5_close_mean_value = day5_close_mean[i]
            day10_close_mean_value = day10_close_mean[i]
            day20_close_mean_value = day20_close_mean[i]
            diff_day5_close = day5_close_mean[i] - day5_close_mean[i + 1]
            diff_day10_close = day10_close_mean[i] - day10_close_mean[i + 1]
            diff_day20_close = day20_close_mean[i] - day20_close_mean[i + 1]
            diff_day5_day10_close = day5_close_mean[i] - day10_close_mean[i]
            diff_day5_day20_close = day5_close_mean[i] - day20_close_mean[i]
            diff_day10_day20_close = day10_close_mean[i] - day20_close_mean[i]
            features = [day5_close_mean_value, day10_close_mean_value, day20_close_mean_value, diff_day5_close,
                        diff_day10_close, diff_day20_close, diff_day5_day10_close,
                        diff_day5_day20_close, diff_day10_day20_close]

            x_all.append(features)

            if close_y[-i - 1] > close_y[-i - 2]:
                if (close_y[-i - 1] / close_y[-i - 2]) - 1 >= 0.05:
                    label = 2
                else:
                    label = 1
            else:
                label = 0
            day_all.append(label)

            if close_y[-i - 1] > close_y[-i - 5]:
                if (close_y[-i - 1] / close_y[-i - 5]) - 1 >= 0.1:
                    label = 2
                else:
                    label = 1
            else:
                label = 0
            week_all.append(label)

            if close_y[-i - 1] > close_y[-i - 20]:
                if (close_y[-i - 1] / close_y[-i - 20]) - 1 >= 0.15:
                    label = 2
                else:
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

        joblib.dump(day_model, stockCode[:-3] + "_MA_day_model.m")
        joblib.dump(week_model, stockCode[:-3] + "_MA_week_model.m")
        joblib.dump(month_model, stockCode[:-3] + "_MA_month_model.m")

        all_mean = [day5_close_mean, day10_close_mean, day20_close_mean]
        return all_mean

    def svm_predict(self, stockCode):
        learnResult = self.svm_learning(stockCode)
        if learnResult is None:
            return None

        day5_close_mean = learnResult[0]
        day10_close_mean = learnResult[1]
        day20_close_mean = learnResult[2]

        features = []
        for i in range(1):
            day5_close_mean_value = day5_close_mean[i]
            day10_close_mean_value = day10_close_mean[i]
            day20_close_mean_value = day20_close_mean[i]
            diff_day5_close = day5_close_mean[i] - day5_close_mean[i + 1]
            diff_day10_close = day10_close_mean[i] - day10_close_mean[i + 1]
            diff_day20_close = day20_close_mean[i] - day20_close_mean[i + 1]
            diff_day5_day10_close = day5_close_mean[i] - day10_close_mean[i]
            diff_day5_day20_close = day5_close_mean[i] - day20_close_mean[i]
            diff_day10_day20_close = day10_close_mean[i] - day20_close_mean[i]
            features = [day5_close_mean_value, day10_close_mean_value, day20_close_mean_value, diff_day5_close,
                        diff_day10_close, diff_day20_close, diff_day5_day10_close,
                        diff_day5_day20_close, diff_day10_day20_close]

        features = np.array(features).reshape(1, -1)
        day_model = joblib.load(stockCode[:-3] + "_MA_day_model.m")
        week_model = joblib.load(stockCode[:-3] + "_MA_week_model.m")
        month_model = joblib.load(stockCode[:-3] + "_MA_month_model.m")

        day_prediction = day_model.predict(features)[0]
        week_prediction = week_model.predict(features)[0]
        month_prediction = month_model.predict(features)[0]
        prediction = [day_prediction, week_prediction, month_prediction]
        return prediction


if __name__ == '__main__':
    code = '002565.SZ'
    AverageStockSelectionUtil().svm_predict(code)
