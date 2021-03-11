# -*- coding: utf-8 -*-
import datetime
import time

import pandas as pd
import tushare as ts


class GetStockPrice(object):
    def __init__(self):
        self.pro = ts.pro_api('2b9929516221569516ff57324dc130c6100a76fa66d4202de854ba58')

    def get_price(self, stock_code, days):
        today = datetime.date.today()
        day60 = today - datetime.timedelta(days=50)
        start_time = day60.strftime("%Y%m%d")
        end_time = time.strftime('%Y%m%d', time.localtime(time.time()))
        df = self.pro.daily(ts_code=stock_code, start_date=start_time, end_date=end_time)
        today_data = df.loc[0]
        pre_data = df.loc[days]
        response_data = {'ts_code': [today_data.trade_date, pre_data.trade_date],
                         'open': [today_data.open, pre_data.open],
                         'high': [today_data.high, pre_data.high],
                         'low': [today_data.low, pre_data.low],
                         'close': [today_data.close, pre_data.close],
                         'pre_close': [today_data.pre_close, pre_data.pre_close]}
        response_data_format = pd.DataFrame(response_data)
        print(response_data_format)


if __name__ == '__main__':
    code = '002565.SZ'
    GetStockPrice().get_price(code, 4)
