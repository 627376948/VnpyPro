# Form implementation generated from reading ui file 'C:\Users\Thinkpad\Desktop\UI\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from vnpy.app.db_viewer.ui.extWidget import DataFrameMonitor
from vnpy.trader.utility import get_icon_path


APP_NAME = "DbViewer"


class DbViewWidget(QtWidgets.QWidget):

    def __init__(self, main_engine, event_engine):
        super(DbViewWidget, self).__init__()
        self.event_engine = event_engine
        self.main_engine = main_engine
        self.appengine = main_engine.get_engine(APP_NAME)
        self.setupUi(self)
        self.retranslateUi(self)
        self.init_event()
        self.showMaximized()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(-1, 6, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_address = QtWidgets.QLabel(self.groupBox_2)
        self.label_address.setObjectName("label_address")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.label_address)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_port = QtWidgets.QLabel(self.groupBox_2)
        self.label_port.setObjectName("label_port")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.label_port)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.label_storage_size = QtWidgets.QLabel(self.groupBox_2)
        self.label_storage_size.setObjectName("label_storage_size")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.label_storage_size)
        self.label_db_state = QtWidgets.QLabel(self.groupBox_2)
        self.label_db_state.setObjectName("label_db_state")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.FieldRole, self.label_db_state)
        self.pushButton_update = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_update.setObjectName("pushButton_update")
        self.formLayout.setWidget(
            5, QtWidgets.QFormLayout.SpanningRole, self.pushButton_update)
        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.tree_select = QtWidgets.QTreeWidget(Form)
        self.tree_select.setObjectName("tree_select")
        self.tree_select.headerItem().setText(0, "选择查看数据库")
        self.gridLayout.addWidget(self.tree_select, 1, 0, 2, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.list_collection_info = QtWidgets.QListWidget(self.groupBox)
        self.list_collection_info.setObjectName("list_collection_info")
        self.horizontalLayout.addWidget(self.list_collection_info)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)
        self.tab_log = QtWidgets.QTabWidget(Form)
        self.tab_log.setTabPosition(QtWidgets.QTabWidget.South)
        self.tab_log.setObjectName("tab_log")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.table_collection = DataFrameMonitor(
            self.appengine, self.event_engine, self.tab)
        self.horizontalLayout_2.addWidget(self.table_collection)
        self.tab_log.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab_2)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_3.addWidget(self.textBrowser)
        self.tab_log.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tab_log, 1, 1, 3, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 6)
        self.gridLayout.setRowStretch(0, 4)
        self.gridLayout.setRowStretch(1, 4)
        self.gridLayout.setRowStretch(2, 16)

        self.retranslateUi(Form)
        self.tab_log.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "数据库监控"))
        self.groupBox_2.setTitle(_translate("Form", "数据库信息"))
        self.label.setText(_translate("Form", "连接地址"))
        self.label_address.setText(_translate("Form", "TextLabel"))
        self.label_3.setText(_translate("Form", "连接状态"))
        self.label_port.setText(_translate("Form", "TextLabel"))
        self.label_5.setText(_translate("Form", "连接端口"))
        self.label_6.setText(_translate("Form", "占用空间"))
        self.label_storage_size.setText(_translate("Form", "TextLabel"))
        self.label_db_state.setText(_translate("Form", "TextLabel"))
        self.pushButton_update.setText(_translate("Form", "立即更新"))
        self.groupBox.setTitle(_translate("Form", "数据集合统计信息"))
        self.tab_log.setTabText(self.tab_log.indexOf(
            self.tab), _translate("Form", "集合列表"))
        self.tab_log.setTabText(self.tab_log.indexOf(
            self.tab_2), _translate("Form", "日志"))

        self.qry_dialog = QueryDialog(self.appengine)

    def init_event(self):

        self.pushButton_update.clicked.connect(self.btn_lick)
        self.tree_select.clicked.connect(self.tree_onclick)
        self.tree_select.doubleClicked.connect(self.tree_ondoubleclick)
        self.appengine.write_log = self.write_log

    def write_log(self, msg):
        self.textBrowser.append(str(msg))

    def btn_lick(self):

        self.appengine.update_db_info()
        self.label_address.setText(self.appengine.db_info["连接地址"])
        self.label_db_state.setText(self.appengine.db_info["连接状态"])
        self.label_port.setText(self.appengine.db_info["连接端口"])
        self.label_storage_size.setText(self.appengine.db_info["占用空间"])
        self.tree_select.setColumnCount(1)
        self.tree_select.clear()
        for db in self.appengine.get_db_names():
            root = QtWidgets.QTreeWidgetItem(self.tree_select)
            root.setText(0, db)
            root.setIcon(0, QtGui.QIcon('dbview.ico'))
            for coll in self.appengine.get_collections_by_dbname(db):
                child = QtWidgets.QTreeWidgetItem(root)
                child.setText(0, coll)
                child.setIcon(0, QtGui.QIcon('collection.ico'))
                root.addChild(child)
            self.tree_select.addTopLevelItem(root)

    def tree_onclick(self):
        try:
            item = self.tree_select.currentItem()
            parent = item.parent()
            if parent == None:
                return None
        except Exception as e:
            return None
        self.write_log(
            f"开始统计{item.text(0)}{'.'*5}{str(datetime.datetime.now())}")
        info = [f"{k}:{v}" for k, v in self.appengine.get_collection_info(
            parent.text(0), item.text(0)).items()]
        self.list_collection_info.clear()
        self.list_collection_info.addItems(info)
        self.write_log(
            f"统计结束{item.text(0)}{'.'*5}{str(datetime.datetime.now())}")

    def tree_ondoubleclick(self):
        try:
            item = self.tree_select.currentItem()
            parent = item.parent()
            if parent == None:
                return None
        except Exception as e:
            return None
        self.write_log(f"开始加载数据{'.'*5}{str(datetime.datetime.now())}")
        self.qry_dialog.update(self.appengine.get_column_names())
        is_accept = self.qry_dialog.exec_()
        if is_accept:
            if self.qry_dialog.form["feild"] == "不筛选":
                datalist = self.appengine.get_data(
                    parent.text(0), item.text(0), limit=self.qry_dialog.form["limit"])
            elif not self.qry_dialog.form["match_date"]:
                flt = {self.qry_dialog.form["feild"]
                    : self.qry_dialog.form["match"]}
                datalist = self.appengine.get_data(
                    parent.text(0), item.text(0), flt=flt, limit=self.qry_dialog.form["limit"])
            elif self.qry_dialog.form["match_date"]:
                if self.qry_dialog.form["match"]:
                    flt = {self.qry_dialog.form["feild"]
                        : self.qry_dialog.form["match"]}
                else:
                    flt = {}
                sample = self.appengine.find_sample(parent.text(0),
                                                    item.text(0))
                datetime_mode = str(sample[self.qry_dialog.form["date_feild"]])
                start = self.appengine.strftime_by_modestr(self.qry_dialog.form["date_start"],
                                                           datetime_mode)
                end = self.appengine.strftime_by_modestr(self.qry_dialog.form["date_end"],
                                                         datetime_mode)
                flt[self.qry_dialog.form["date_feild"]] = {
                    "$gte": start, "$lte": end}

                datalist = self.appengine.get_data(
                    parent.text(0), item.text(0), flt=flt, limit=self.qry_dialog.form["limit"])

            if datalist:
                try:
                    self.table_collection.update_by_list(datalist)
                    self.write_log(
                        f"加载成功{'.'*5}{str(datetime.datetime.now())}")
                    self.write_log(f"筛选条件{self.qry_dialog.form}")
                except Exception as e:
                    self.write_log("加载失败{self.qry_dialog.form}")
        else:
            self.write_log(f"取消加载数据{'.'*5}{str(datetime.datetime.now())}")


class QueryDialog(QtWidgets.QDialog):

    def __init__(self, appengine):
        super(QueryDialog, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.form = {}
        self.appengine = appengine
        self.init_event()
        self.update_form()

    def update(self, column_names):
        self.checkBox_all.setChecked(False)
        self.lineEdit_limit.setEnabled(True)
        self.lineEdit_limit.setText("100")
        self.comboBox_feild.clear()
        self.comboBox_feild.addItems(["不筛选"])
        self.comboBox_feild.addItems(column_names)
        self.lineEdit_matchtext.setText("")
        self.lineEdit_matchtext.setEnabled(False)
        self.comboBox_datetime_feild.setEnabled(False)
        self.checkBox_datetime.setChecked(False)
        self.comboBox_datetime_feild.clear()
        date_feild = [x for x in column_names
                      if "date" in x]
        self.comboBox_datetime_feild.addItems(date_feild)
        self.dateEdit_start.setEnabled(False)
        self.dateEdit_end.setEnabled(False)

    def init_event(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.accepted.connect(self.update_form)
        self.buttonBox.rejected.connect(self.reject)
        self.checkBox_all.stateChanged['int'].connect(
            self.change_limit_state)
        self.checkBox_datetime.stateChanged['int'].connect(
            self.change_field_state)
        self.comboBox_feild.currentTextChanged.connect(self.change_feild)
        QtCore.QMetaObject.connectSlotsByName(self)

    def update_form(self):
        self.form["limit"] = 0 if self.checkBox_all.isChecked(
        ) else int(self.lineEdit_limit.text())
        self.form["feild"] = self.comboBox_feild.currentText()
        self.form["match"] = self.lineEdit_matchtext.text()
        self.form["match_date"] = self.checkBox_datetime.isChecked()
        self.form["date_feild"] = self.comboBox_datetime_feild.currentText()
        self.form["date_start"] = self.dateEdit_start.date().toPyDate()
        self.form["date_end"] = self.dateEdit_end.date().toPyDate()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 150)
        self.formLayout = QtWidgets.QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")
        self.checkBox_all = QtWidgets.QCheckBox(Dialog)
        self.checkBox_all.setEnabled(True)
        self.checkBox_all.setAcceptDrops(False)
        self.checkBox_all.setToolTip("")
        self.checkBox_all.setChecked(True)
        self.checkBox_all.setObjectName("checkBox_all")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.checkBox_all)
        self.lineEdit_limit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_limit.setText("100")
        self.lineEdit_limit.setObjectName("lineEdit_limit")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_limit)
        self.comboBox_feild = QtWidgets.QComboBox(Dialog)
        self.comboBox_feild.setObjectName("comboBox_feild")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.comboBox_feild)
        self.lineEdit_matchtext = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_matchtext.setObjectName("lineEdit_matchtext")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_matchtext)
        self.checkBox_datetime = QtWidgets.QCheckBox(Dialog)
        self.checkBox_datetime.setObjectName("checkBox_datetime")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.checkBox_datetime)
        self.comboBox_datetime_feild = QtWidgets.QComboBox(Dialog)
        self.comboBox_datetime_feild.setObjectName("comboBox_datetime_feild")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.comboBox_datetime_feild)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(
            5, QtWidgets.QFormLayout.FieldRole, self.buttonBox)
        self.dateEdit_start = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_start.setObjectName("dateEdit_start")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.dateEdit_start)
        self.dateEdit_end = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_end.setObjectName("dateEdit_end")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.FieldRole, self.dateEdit_end)

        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.checkBox_all.setText(_translate("Dialog", "所有数据"))
        self.checkBox_datetime.setText(_translate("Dialog", "选择区间"))
        self.label.setText(_translate("Dialog", "起始日期"))
        self.label_2.setText(_translate("Dialog", "截至日期"))

    def change_limit_state(self, is_checked):
        if is_checked:
            self.lineEdit_limit.setEnabled(False)
        else:
            self.lineEdit_limit.setEnabled(True)

    def change_field_state(self, is_checked):
        if is_checked:
            self.comboBox_datetime_feild.setEnabled(True)
            self.dateEdit_start.setEnabled(True)
            self.dateEdit_end.setEnabled(True)
        else:
            self.comboBox_datetime_feild.setEnabled(False)
            self.dateEdit_start.setEnabled(False)
            self.dateEdit_end.setEnabled(False)

    def change_feild(self, change_str):
        if change_str == "不筛选":
            self.lineEdit_matchtext.setEnabled(False)
        else:
            self.lineEdit_matchtext.setEnabled(True)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from vnpy.app.db_viewer import DbViewApp
    from vnpy.trader.engine import MainEngine

    main_engine = MainEngine()
    main_engine.add_app(DbViewApp)
    app = QApplication(sys.argv)
    w = DbViewWidget(main_engine, None)
    w.show()
    sys.exit(app.exec_())
