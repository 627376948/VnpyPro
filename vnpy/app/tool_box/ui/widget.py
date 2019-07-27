# encoding: UTF-8

'''
app记录模块相关的GUI控制组件
'''
import datetime
import inspect
import os

from PyQt5 import QtWidgets, QtCore, QtGui

from vnpy.app.tool_box.engine import APP_NAME, CHINESE
from vnpy.app.tool_box.ui.monitor import DataFrameMonitor
from vnpy.app.tool_box.util import get_jsonpath
from vnpy.event import Event


class ToolBoxWidget(QtWidgets.QWidget):
    """工具箱组件"""
    signal = QtCore.pyqtSignal(Event)
    icon_filename = 'func.ico'
    icon_file_path = get_jsonpath(icon_filename, __file__)

    def __init__(self, main_engine, event_engine):
        """Constructor"""
        super(ToolBoxWidget, self).__init__()
        self.event_engine = event_engine
        self.main_engine = main_engine
        self.app_engine = main_engine.get_engine(APP_NAME)
        self.setupUi(self)
        self.retranslateUi(self)
        self.file_viewer = None
        self.init_func_action()
        self.init_menu()
        self.register_event()
        self.showMaximized()

    def setupUi(self, ToolWidget):
        ToolWidget.setObjectName("ToolWidget")
        ToolWidget.resize(1095, 662)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ToolWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(ToolWidget)
        self.groupBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.listWidget = QtWidgets.QListWidget(self.groupBox)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout.addWidget(self.groupBox)
        self.stackedWidget = QtWidgets.QStackedWidget(ToolWidget)
        self.stackedWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.stackedWidget.setObjectName("stackedWidget")
        self.horizontalLayout.addWidget(self.stackedWidget)
        self.groupBox_2 = QtWidgets.QGroupBox(ToolWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.output_result = DataFrameMonitor(
            self.main_engine, self.event_engine)
        self.output_result.sorting = True
        self.verticalLayout.addWidget(self.output_result)
        self.output_log = QtWidgets.QTextBrowser(self.groupBox_2)
        self.output_log.setMaximumSize(QtCore.QSize(16777215, 200))
        self.verticalLayout.addWidget(self.output_log)
        self.horizontalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(ToolWidget)
        QtCore.QMetaObject.connectSlotsByName(ToolWidget)

    def retranslateUi(self, ToolWidget):
        _translate = QtCore.QCoreApplication.translate
        ToolWidget.setWindowTitle(_translate("ToolWidget", "Form"))
        self.groupBox.setTitle(_translate("ToolWidget", "工具栏"))
        self.groupBox_2.setTitle(_translate("ToolWidget", "显示栏"))

    def init_func_action(self):
        """"""
        appfuncs = dir(self.app_engine)
        func_names = [x for x in appfuncs if x.startswith("do_")]
        for func_name in func_names:
            item = QtWidgets.QListWidgetItem(
                QtGui.QIcon(self.icon_file_path), CHINESE[func_name])
            self.listWidget.addItem(item)
#             self.listWidget.addItem(
#                 QtWidgets.QListWidgetItem(CHINESE[func_name]))
            func = getattr(self.app_engine, func_name)
            b = inspect.getfullargspec(func)
            kwargs = []
            for k, v in zip(b.args[1:], b.defaults):
                kwarg = (k, v)
                kwargs.append(kwarg)
#             action_func = partial(self.active_function, func_name)
            w = Inputer(func_name, kwargs, self)
            self.stackedWidget.addWidget(w)

    def active_function(self, func_name, **kwargs):

        begin = datetime.datetime.now()
        self.write_log(f"函数执行开始：{str(begin)}")
        func = getattr(self.app_engine, func_name)
#         print(f"函数执行开始：{str(begin)}:{func.__name__}")
#         print(f"函数执行开始：{str(begin)}:{str(kwargs)}")
        res = func(**kwargs)
        print(str(res[0]))
        if res[0]:
            self.update_reslut(res[1])
        else:
            self.write_log(res[1])
        end = datetime.datetime.now()
        time_delta = end - begin
        self.write_log(f"函数执行结束：用时{str(time_delta)}秒")

    def write_log(self, context):
        """更新日志"""
        self.output_log.append(context)

    def update_reslut(self, resluts):
        try:
            self.output_result.update_by_list(resluts)
        except Exception as e:
            self.write_log(str(e))

    def register_event(self):
        """注册事件监听"""
        self.listWidget.currentRowChanged.connect(self.change_inputer)
        self.listWidget.doubleClicked.connect(self.display_inputer)
        self.output_result.cellDoubleClicked.connect(self.open_file)
#         self.search_thread.reslut_signal.connect(self.update_reslut)
#         self.search_thread.log_signal.connect(self.write_log)

    def change_inputer(self, i):
        """"""
        self.stackedWidget.setCurrentIndex(i)

    def display_inputer(self, item):
        """"""
        if self.stackedWidget.isVisible():
            self.stackedWidget.setVisible(False)
        else:
            self.stackedWidget.setVisible(True)

    def open_file(self, x, y):
        # 点击的是第一列
        if y == 0:
            try:
                os.startfile(self.output_result.item(x, 1).text())
            except Exception as e:
                self.write_log(e)
        # 点击的是第二列
        if y == 1:
            try:
                os.startfile(os.path.split(
                    self.output_result.item(x, 1).text())[0])
            except Exception as e:
                self.write_log(e)

    def init_menu(self):
        """"""

        def clear_xls():
            """"""
            items = self.output_result.selectedItems()
            xls_files = [item.text() for item in items]
            context = self.app_engine.clear_xls(xls_files, "企业内部员工编号")
            self.write_log(context)

        clearAction = QtWidgets.QAction("清除xls冗余", self.output_result)
        self.output_result.menu.addAction(clearAction)
        clearAction.triggered.connect(clear_xls)

    def keyPressEvent(self, event):
        """"""

        def show_searcher_widget():
            """"""
            if self.file_viewer:
                self.file_viewer.show()
            else:
                self.file_viewer = FileViewer(
                    self.app_engine, self.event_engine, None)
                self.file_viewer.show()

        if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.AltModifier \
                and event.key() == QtCore.Qt.Key_F:
            show_searcher_widget()


class Inputer(QtWidgets.QWidget):

    def __init__(self, func_name, kwagrs_tuple, parent=None):
        super(Inputer, self).__init__(parent)
        self.parent = parent
        self.app_engine = parent.app_engine
        self.kwagrs_tuple = kwagrs_tuple
        self.func = parent.active_function
        self.func_name = func_name
        self.setting = {}
        self.input_int = {}
        self.input_str = {}
        self.input_list = {}
        self.input_bool = {}
        # 初始化ui
        self.load_setting()
        self.init_ui()
        # 注册事件
        self.register_event()

    def init_ui(self):

        self.vbox = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.vbox)
        self.submit_bt = QtWidgets.QPushButton("启动工具")
        self.vbox.addWidget(QtWidgets.QLabel(CHINESE[self.func_name]))
        self.vbox.addWidget(self.submit_bt)

        for tuple in self.kwagrs_tuple:
            name, value = tuple
            text = QtWidgets.QLabel(CHINESE[name])
#             self.setting.update({name: value})
            value = self.setting.get(name, value)
            d = {}
            self.vbox.addWidget(text)
            if isinstance(value, int):
                d = self.input_int
            elif isinstance(value, bool):
                d = self.input_bool
            elif isinstance(value, list):
                d = self.input_list
            elif isinstance(value, str):
                d = self.input_str
            d[name] = QtWidgets.QLineEdit(str(value))
            self.vbox.addWidget(d[name])
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vbox.addItem(spacerItem)

    def register_event(self):
        """"""
        self.submit_bt.clicked.connect(self.submit)

    def submit(self):
        """"""
        for k, y in self.input_str.items():

            if k == "dir_path":
                dir_path = QtWidgets.QFileDialog.getExistingDirectory(
                    self, k, y.text())
                if dir_path:
                    y.setText(os.path.abspath(dir_path))
                else:
                    self.write_log("输入文件目录错误")
                    return
            if k == "file_path":
                file_path, file_type = QtWidgets.QFileDialog.getOpenFileName(
                    self, k, 'data', 'XLS(*.xls)')
                if file_path:
                    y.setText(os.path.abspath(file_path))
                else:
                    self.write_log("输入文件错误")
                    return
        self.write_log(str(self.kwagrs))
        self.parent.active_function(self.func_name, **self.kwagrs)
        self.save_setting(self.kwagrs)

    def write_log(self, context):
        """"""
        self.parent.write_log(str(context))

    def load_setting(self):
        """"""
        all_setting = self.app_engine.load_setting()
        func_setting = {k.split(".")[1]: v for k,
                        v in all_setting.items() if f"{self.func_name}." in k}
        self.setting.update(func_setting)

    def save_setting(self, dict):
        """"""
        d = {f"{self.func_name}.{k}": v for k,
             v in dict.items()}
        self.app_engine.save_setting(d)

    @property
    def kwagrs(self):
        """"""
        for k, y in self.input_int.items():
            self.setting.update({k: int(y.text())})
        for k, y in self.input_str.items():
            self.setting.update({k: y.text()})
        return self.setting


class WorkThread(QtCore.QThread):
    """"""
    reslut_signal = QtCore.pyqtSignal(list)
    log_signal = QtCore.pyqtSignal(str)
    setting_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, func_name, kwargs, app_wideget):
        super(WorkThread, self).__init__()
        self.func_name = func_name
        self.kwargs = kwargs
        self.app_wideget = app_wideget
        self.active = False

    def run(self):
        if not self.active:
            begin = datetime.datetime.now()
            self.log_signal.emit(f"查询开始：{str(begin)}")
            self.active = True
            res = self.app_wideget.active_function(
                self.func_name, **self.kwargs)
            if res[0]:
                self.reslut_signal.emit(res[1])
            else:
                self.log_signal.emit(res[1])
            end = datetime.datetime.now()
            time_delta = end - begin
            self.log_signal.emit(f"查询结束：用时{str(time_delta)}秒")
            self.active = False

        else:
            self.log_signal.emit(f"后台工作中，请稍后再操作工具")


class FileViewer(QtWidgets.QWidget):

    def __init__(self, app_engine, event_engine, parent=None):
        super(FileViewer, self).__init__(parent)
        self.app_engine = app_engine
        self.event_engine = event_engine
        self.setWindowTitle("数据查询工具")
        # 初始化ui
        self.init_ui()
        # 初始化设置
#         self.load_setting()
#         # 注册事件
#         self.register_event()

    def init_ui(self):
        self.resize(1000, 560)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setTitle("查询信息")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setText("关键字:")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setText("")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setText("数据源:")
        self.horizontalLayout.addWidget(self.label_2)
        self.comboBox_data_table = QtWidgets.QComboBox(self.groupBox)
        self.horizontalLayout.addWidget(self.comboBox_data_table)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setText("查询字段:")
        self.horizontalLayout.addWidget(self.label_3)
        self.comboBox_field = QtWidgets.QComboBox(self.groupBox)
        self.horizontalLayout.addWidget(self.comboBox_field)
        self.gridLayout.addWidget(self.groupBox, 0, 2, 1, 1)

        self.groupBox_2 = QtWidgets.QGroupBox(self)
        self.groupBox_2.setTitle("查询结果")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableView = DataFrameMonitor(None, None, self)
        self.gridLayout_2.addWidget(self.tableView, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 2, 1, 1)
        self.setLayout(self.gridLayout)

    def load_setting(self):
        """"""

        for table_name in self.app_engine.get_xls_tables():
            self.comboBox_data_table.addItem(table_name, None)
            self.update_comboBox(Qstring=self.app_engine.get_xls_tables()[0])

        if "联系人表" in self.app_engine.get_xls_tables():
            self.comboBox_data_table.setCurrentText("2019年联系人表")
            self.comboBox_field.setCurrentText("联系人姓名")

        self.tableView.sorting = True

    def register_event(self):
        self.comboBox_data_table.currentTextChanged.connect(
            self.update_comboBox)
        self.lineEdit.returnPressed.connect(self.qry_keywords)

    def update_comboBox(self, Qstring):
        self.comboBox_field.clear()
        for col_name in self.app_engine.get_xls_col_names(Qstring):
            self.comboBox_field.addItem(col_name, None)

    def qry_keywords(self):
        try:
            resluts = self.app_engine.qry_xls_info(self.lineEdit.text(),
                                                   self.comboBox_data_table.currentText(),
                                                   self.comboBox_field.currentText())
            self.tableView.update_by_list(resluts)
        except Exception as e:
            error_msg = [
                {"提示": "查询报错", "说明": "查无此信息，输入关键字没有找到匹配项", "具体报错": str(e)}]
            self.tableView.update_by_list(error_msg)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    from vnpy.app.tool_box import ToolBoxApp
    from vnpy.app.tool_box.engine import ToolBoxEngine
    from vnpy.app.tool_box.ui.widget import ToolBoxWidget
    from vnpy.trader.engine import MainEngine, EventEngine
    import sys
    import qdarkstyle
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    icon = QtGui.QIcon("app.png")
    app.setWindowIcon(icon)
    ee = EventEngine()
    me = MainEngine(ee)
    me.add_app(ToolBoxApp)
    tb = ToolBoxEngine(me, ee)
    ui = ToolBoxWidget(me, ee)
    ui.setWindowTitle("桌面工具")
    ui.showMaximized()

    ee.stop()
    sys.exit(app.exec_())
