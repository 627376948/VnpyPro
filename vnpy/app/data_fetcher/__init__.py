from pathlib import Path

from vnpy.trader.app import BaseApp
from .engine import APP_NAME, DataFetchEngine


class DataFetchApp(BaseApp):
    """"""

    app_name = APP_NAME
    app_module = __module__
    app_path = Path(__file__).parent
    display_name = "数据本地化"
    engine_class = DataFetchEngine
    widget_name = "DataFetchWidget"
    icon_name = "fetcher.ico"
