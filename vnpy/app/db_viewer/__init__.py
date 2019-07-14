from pathlib import Path

from vnpy.trader.app import BaseApp
from .engine import APP_NAME, DbViewEngine


class DbViewApp(BaseApp):
    """"""

    app_name = APP_NAME
    app_module = __module__
    app_path = Path(__file__).parent
    display_name = "数据库监测"
    engine_class = DbViewEngine
    widget_name = "DbViewWidget"
    icon_name = "dbview.ico"
