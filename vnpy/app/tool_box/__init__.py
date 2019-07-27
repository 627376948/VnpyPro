from pathlib import Path
from vnpy.trader.app import BaseApp
from .engine import APP_NAME, ToolBoxEngine


class ToolBoxApp(BaseApp):
    """"""

    app_name = APP_NAME
    app_module = __module__
    app_path = Path(__file__).parent
    display_name = "CMY桌面工具"
    engine_class = ToolBoxEngine
    widget_name = "ToolBoxWidget"
    icon_name = "app.png"
