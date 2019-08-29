from datetime import datetime, timedelta
from typing import List
import time

from pymongo import MongoClient

import pandas as pd
from .constant import Exchange, Interval
from .object import BarData, HistoryRequest
from .setting import SETTINGS

# from rqdatac import init as rqdata_init
# from rqdatac.services.basic import all_instruments as rqdata_all_instruments
# from rqdatac.services.get_price import get_price as rqdata_get_price
# from rqdatac.share.errors import AuthenticationFailed
INTERVAL_VT2RQ = {
    Interval.MINUTE:
    "1min",
    #     Interval.FIVEMINUTE: "5min",
    #     Interval.FIFTEENMINUTE: "15min",
    #     Interval.THIRTYMINUTE: "30min",
    Interval.HOUR:
    "60min",
    Interval.DAILY:
    "1d",
}

INTERVAL_ADJUSTMENT_MAP = {
    Interval.MINUTE: timedelta(minutes=1),
    Interval.HOUR: timedelta(hours=1),
    Interval.DAILY: timedelta()  # no need to adjust for daily bar
}


class RqdataClient:
    """
    Client for querying history data from MongoDB.
    """
    def __init__(self):
        """"""
        self.username = SETTINGS["database.user"]
        self.password = SETTINGS["database.password"]
        self.host = SETTINGS["database.host"]
        self.port = SETTINGS["database.port"]
        self.db_client = MongoClient(self.host, int(self.port))
        self.authentication_source = SETTINGS["database.authentication_source"]
        self.inited = False
        self.symbols = set()

    def init(self, username="", password=""):
        """"""
        if self.inited:
            return True

        if username and password:
            self.username = username
            self.password = password


#         rqdata_init(self.username, self.password,
#                     ('rqdatad-pro.ricequant.com', 16011))
        try:
            ls = [x for x in self.db_client["quantaxis"]["etf_list"].find({})]
            df = pd.DataFrame(ls)
            for ix, row in df.iterrows():
                self.symbols.add(row['code'])
            ls = [
                x for x in self.db_client["quantaxis"]["stock_list"].find({})
            ]
            df = pd.DataFrame(ls)
            for ix, row in df.iterrows():
                self.symbols.add(row['code'])
        except (RuntimeError):
            return False

        self.inited = True
        return True

    def to_rq_symbol(self, symbol: str, exchange: Exchange):
        """
        CZCE product of RQData has symbol like "TA1905" while
        vt symbol is "TA905.CZCE" so need to add "1" in symbol.
        """
        return symbol

    def query_history(self, req: HistoryRequest):
        """
        Query history bar data from RQData.
        """
        symbol = req.symbol
        exchange = req.exchange
        interval = req.interval
        start = int(time.mktime(req.start.timetuple()))
        end = int(time.mktime(req.end.timetuple()))

        rq_symbol = self.to_rq_symbol(symbol, exchange)
        if rq_symbol not in self.symbols:
            print(1)
            return None

        rq_interval = INTERVAL_VT2RQ.get(interval)
        if not rq_interval:
            print(2)
            return None

        # For adjust timestamp from bar close point (RQData) to open point (VN
        # Trader)
        adjustment = INTERVAL_ADJUSTMENT_MAP[interval]

        # For querying night trading period data
        #         end += timedelta(1)
        if rq_interval == "1d":
            if rq_symbol[:2] == "15" or rq_symbol[:2] == "51":
                ls = [
                    x for x in self.db_client["quantaxis"]["index_day"].find({
                        "code":
                        rq_symbol,
                        "date_stamp": {
                            "$gte": start,
                            "$lte": end
                        }
                    })
                ]
                df = pd.DataFrame(ls)
            else:
                ls = [
                    x for x in self.db_client["quantaxis"]["stock_day"].find({
                        "code":
                        rq_symbol,
                        "date_stamp": {
                            "$gte": start,
                            "$lte": end
                        }
                    })
                ]
                df = pd.DataFrame(ls)
        else:
            if rq_symbol[:2] == "15" or rq_symbol[:2] == "51":
                ls = [
                    x for x in self.db_client["quantaxis"]["index_min"].find(
                        {
                            "code": rq_symbol,
                            "tyoe": rq_interval,
                            "time_stamp": {
                                "$gte": start,
                                "$lte": end
                            }
                        })
                ]
                df = pd.DataFrame(ls)
            else:
                ls = [
                    x for x in self.db_client["quantaxis"]["stock_min"].find(
                        {
                            "code": rq_symbol,
                            "tyoe": rq_interval,
                            "time_stamp": {
                                "$gte": start,
                                "$lte": end
                            }
                        })
                ]
                df = pd.DataFrame(ls)

        data: List[BarData] = []

        if df is not None:
            for ix, row in df.iterrows():
                if rq_interval == "1d":
                    d = datetime.fromtimestamp(row["date_stamp"])
                else:
                    d = datetime.fromtimestamp(row["time_stamp"])
                bar = BarData(symbol=symbol,
                              exchange= exchange,
                              interval= interval,
                              datetime= d - adjustment,
                              open_price=row["open"],
                              high_price=row["high"],
                              low_price=row["low"],
                              close_price=row["close"],
                              volume=row["vol"],
                              gateway_name="RQ")
                data.append(bar)

        return data

rqdata_client = RqdataClient()
