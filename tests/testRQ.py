# coding:UTF-8
"""
模块简介:
主要功能：

作者：CJY
"""


import datetime,sys
sys.path.insert(0,r"F:\9.workspace\VnpyPro")
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import HistoryRequest
from vnpy.trader.rqdata import RqdataClient


if __name__ == '__main__':
    """here to test model"""
    rqdata_client = RqdataClient()

# 1m,d
    vt_symbol = "600340"
    start = datetime.datetime(2017, 1, 1)
    end = datetime.datetime(2018, 1, 1)
    interval = Interval.DAILY
    req = HistoryRequest(vt_symbol, start=start, end=end,
                         interval=interval, exchange=Exchange.SSE)
    print(rqdata_client.init())
    for x in rqdata_client.query_history(req):
        print(x.__dict__.get("datetime",None))
