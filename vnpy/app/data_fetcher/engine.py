"""
Author: Zehua Wei (nanoric)

Load data from a csv file.

Differences to 1.9.2:
    * combine Date column and Time column into one Datetime column

Sample csv file:

```csv
"Datetime","Open","High","Low","Close","Volume"
2010-04-16 09:16:00,3450.0,3488.0,3450.0,3468.0,489
2010-04-16 09:17:00,3468.0,3473.8,3467.0,3467.0,302
2010-04-16 09:18:00,3467.0,3471.0,3466.0,3467.0,203
2010-04-16 09:19:00,3467.0,3468.2,3448.0,3448.0,280
2010-04-16 09:20:00,3448.0,3459.0,3448.0,3454.0,250
2010-04-16 09:21:00,3454.0,3456.8,3454.0,3456.8,109
```

"""

from datetime import datetime
from typing import TextIO
import csv

from vnpy.event import EventEngine
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import database_manager
from vnpy.trader.engine import BaseEngine, MainEngine
from vnpy.trader.object import BarData


APP_NAME = "DataFetcher"


class DataFetchEngine(BaseEngine):
    """"""

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        """"""
        super().__init__(main_engine, event_engine, APP_NAME)
