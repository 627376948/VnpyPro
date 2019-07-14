# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Thinkpad\Desktop\UI\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(QtWidgets.QWidget):

    def __init__(self, event_engine, appengine):
        super(Ui_Form, self).__init__()
        self.event_engine = event_engine
        self.appengine = appengine
        self.setupUi(self)
        self.retranslateUi(self)
        self.collections = {}
        self.db_client = appengine.db_client if appengine else None
        self.db_info = {}
        self.collections_info = {}

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
        self.tree_select.headerItem().setText(0, "1")
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
        self.table_collection = QtWidgets.QTableWidget(self.tab)
        self.table_collection.setObjectName("table_collection")
        self.table_collection.setColumnCount(0)
        self.table_collection.setRowCount(0)
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


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Ui_Form(None, None)
    w.show()
    sys.exit(app.exec_())
