# coding:UTF-8
"""
模块简介:
主要功能：

作者：CJY
"""


import datetime

from vnpy.vnpy.trader.constant import Exchange, Interval
from vnpy.vnpy.trader.object import HistoryRequest
from vnpy.vnpy.trader.rqdata import RqdataClient


if __name__ == '__main__':
    """here to test model"""
    rqdata_client = RqdataClient()

# 1m,d
    vt_symbol = "000001"
    start = datetime.datetime(2017, 1, 1)
    end = datetime.datetime(2018, 1, 1)
    interval = Interval.DAILY
    req = HistoryRequest(vt_symbol, start=start, end=end,
                         interval=interval, exchange=Exchange.SSE)
    print(rqdata_client.init())
    for x in rqdata_client.query_history(req):
        print(x)
