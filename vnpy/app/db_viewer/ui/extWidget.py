# coding:UTF-8
"""
模块简介:
主要功能：

作者：CJY
"""
from collections import OrderedDict
import csv
import traceback

from PyQt5 import QtWidgets, QtGui
from pandas import DataFrame


EVENT_DISPLAY_DATAFRAME = 'eDataFrme'
EVENT_DRAW_FIGURE = 'eFigure'


class FrameCell(QtWidgets.QTableWidgetItem):
    """DataFrame基础的单元格"""

    def __init__(self, text=None):
        """Constructor"""
        super(FrameCell, self).__init__()
        self.setText(str(text))


class BasicMonitor(QtWidgets.QTableWidget):
    """
    基础监控

    headerDict中的值对应的字典格式如下
    {'chinese': u'中文名', 'cellType': BasicCell}

    """

    #----------------------------------------------------------------------
    def __init__(self, mainEngine=None, eventEngine=None, parent=None):
        """Constructor"""
        super(BasicMonitor, self).__init__(parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        # 保存表头标签用
        self.headerDict = OrderedDict()  # 有序字典，key是英文名，value是对应的配置字典
        self.headerList = []             # 对应self.headerDict.keys()

        # 保存相关数据用
        self.dataDict = {}  # 字典，key是字段对应的数据，value是保存相关单元格的字典
        self.dataKey = ''   # 字典键对应的数据字段

        # 监控的事件类型
        self.eventType = ''

        # 列宽调整状态（只在第一次更新数据时调整一次列宽）
        self.columnResized = False

        # 字体
        self.font = None

        # 保存数据对象到单元格
        self.saveData = False

        # 默认不允许根据表头进行排序，需要的组件可以开启
        self.sorting = False

        # 初始化右键菜单
        self.initMenu()

    #----------------------------------------------------------------------
    def setHeaderDict(self, headerDict):
        """设置表头有序字典"""
        self.headerDict = headerDict
        self.headerList = headerDict.keys()

    #----------------------------------------------------------------------
    def setDataKey(self, dataKey):
        """设置数据字典的键"""
        self.dataKey = dataKey

    #----------------------------------------------------------------------
    def setEventType(self, eventType):
        """设置监控的事件类型"""
        self.eventType = eventType

    #----------------------------------------------------------------------
    def setFont(self, font):
        """设置字体"""
        self.font = font

    #----------------------------------------------------------------------
    def setSaveData(self, saveData):
        """设置是否要保存数据到单元格"""
        self.saveData = saveData

    #----------------------------------------------------------------------
    def initTable(self):
        """初始化表格"""
        # 设置表格的列数
        col = len(self.headerDict)
        self.setColumnCount(col)

        # 设置列表头
        labels = [d['chinese'] for d in self.headerDict.values()]
        self.setHorizontalHeaderLabels(labels)

        # 关闭左边的垂直表头
        self.verticalHeader().setVisible(False)

        # 设为不可编辑
        self.setEditTriggers(self.NoEditTriggers)

        # 设为行交替颜色
        self.setAlternatingRowColors(True)

        # 设置允许排序
        self.setSortingEnabled(self.sorting)

    #----------------------------------------------------------------------
    def registerEvent(self):
        """注册GUI更新相关的事件监听"""
        pass
    #----------------------------------------------------------------------

    def updateEvent(self, event):
        """收到事件更新"""
        data = event.dict_['data']
        self.updateData(data)

    #----------------------------------------------------------------------
    def updateData(self, data):
        """将数据更新到表格中"""
        # 如果允许了排序功能，则插入数据前必须关闭，否则插入新的数据会变乱
        if self.sorting:
            self.setSortingEnabled(False)

        # 如果设置了dataKey，则采用存量更新模式
        if self.dataKey:
            key = data.__getattribute__(self.dataKey)
            # 如果键在数据字典中不存在，则先插入新的一行，并创建对应单元格
            if key not in self.dataDict:
                self.insertRow(0)
                d = {}
                for n, header in enumerate(self.headerList):
                    content = data.__getattribute__(header)
                    cellType = self.headerDict[header]['cellType']
                    cell = cellType(content, self.mainEngine)

                    if self.font:
                        cell.setFont(self.font)  # 如果设置了特殊字体，则进行单元格设置

                    if self.saveData:            # 如果设置了保存数据对象，则进行对象保存
                        cell.data = data

                    self.setItem(0, n, cell)
                    d[header] = cell
                self.dataDict[key] = d
            # 否则如果已经存在，则直接更新相关单元格
            else:
                d = self.dataDict[key]
                for header in self.headerList:
                    content = data.__getattribute__(header)
                    cell = d[header]
                    cell.setContent(content)

                    if self.saveData:            # 如果设置了保存数据对象，则进行对象保存
                        cell.data = data
        # 否则采用增量更新模式
        else:
            self.insertRow(0)
            for n, header in enumerate(self.headerList):
                content = data.__getattribute__(header)
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content, self.mainEngine)

                if self.font:
                    cell.setFont(self.font)

                if self.saveData:
                    cell.data = data

                self.setItem(0, n, cell)

        # 调整列宽
        if not self.columnResized:
            self.resizeColumns()
            self.columnResized = True

        # 重新打开排序
        if self.sorting:
            self.setSortingEnabled(True)

    #----------------------------------------------------------------------
    def resizeColumns(self):
        """调整各列的大小"""
        self.horizontalHeader().resizeSections(QtWidgets.QHeaderView.ResizeToContents)

    #----------------------------------------------------------------------
    def setSorting(self, sorting):
        """设置是否允许根据表头排序"""
        self.sorting = sorting

    #----------------------------------------------------------------------
    def saveToCsv(self):
        """保存表格内容到CSV文件"""
        # 先隐藏右键菜单
        self.menu.close()

        # 获取想要保存的文件名
        path, fileType = QtWidgets.QFileDialog.getSaveFileName(
            self, "保存数据", 'data', 'CSV(*.csv)')

        try:
            # if not path.isEmpty():
            if path:
                with open(path, 'w', newline="") as f:
                    writer = csv.writer(f)
                    # 保存标签
                    headers = [header for header in self.headerList]
                    writer.writerow(headers)
                    # 保存每行内容
                    for row in range(self.rowCount()):
                        rowdata = []
                        for column in range(self.columnCount()):
                            item = self.item(row, column)
                            if item is not None:
                                rowdata.append(item.text())
                            else:
                                rowdata.append('')
                        writer.writerow(rowdata)
        except Exception as e:
            print(e)
            traceback.print_exc()

    def saveToXls(self):
        """保存表格内容到XLS文件"""
        # 先隐藏右键菜单
        self.menu.close()
        path, fileType = QtWidgets.QFileDialog.getSaveFileName(
            self, "保存数据", 'data', 'XLS(*.xls)')
        try:
            # if not path.isEmpty():
            if path:
                df = self.getDataFrame()
                df.to_excel(path)
        except Exception as e:
            print(e)
            traceback.print_exc()
    #----------------------------------------------------------------------

    def initMenu(self):
        """初始化右键菜单"""
        self.menu = QtWidgets.QMenu(self)

        resizeAction = QtWidgets.QAction("调整列宽", self)
        resizeAction.triggered.connect(self.resizeColumns)

        saveAction = QtWidgets.QAction("保存为csv", self)
        saveAction.triggered.connect(self.saveToCsv)

        saveAction2 = QtWidgets.QAction("保存为xls", self)
        saveAction2.triggered.connect(self.saveToXls)

        self.menu.addAction(resizeAction)
        self.menu.addAction(saveAction)
        self.menu.addAction(saveAction2)

    #----------------------------------------------------------------------
    def contextMenuEvent(self, event):
        """右键点击事件"""
        self.menu.popup(QtGui.QCursor.pos())

    def getDataFrame(self):
        """从表格获取为dataFrame格式数据"""
        try:
            # 保存标签
            headers = self.headerList
            list_ = []
            # 保存每行内容
            for row in range(self.rowCount()):
                rowdata = []
                for column in range(self.columnCount()):
                    item = self.item(row, column)
                    if item is not None:
                        rowdata.append(item.text())
                    else:
                        rowdata.append('')
                list_.append(rowdata)
            return DataFrame(list_, columns=headers)

        except IOError as e:
            raise e


class DataFrameMonitor(BasicMonitor):
    """
     用于通用化DataFrame数据的监控  
    """
    name = u"DataFrame监控"

    def __init__(self,   mainEngine, eventEngine, parent=None):
        """Constructor"""
        super(DataFrameMonitor, self).__init__(mainEngine, eventEngine, parent)
        # 列宽调整状态（只在第一次更新数据时调整一次列宽）
        self.columnResized = False
        # 保存数据对象到单元格
        self.saveData = False
        # 默认不允许根据表头进行排序，需要的组件可以开启
        self.sorting = True
        # 初始化右键菜单
        self.setEventType(EVENT_DISPLAY_DATAFRAME)
        self.registerEvent()

    def updateData(self, data, lastRow=False):
        """将数据更新到表格中,默认在最后一行更新，False则为首行更新"""
        if lastRow:
            updateRow = self.rowCount()
        else:
            updateRow = 0
        # 如果允许了排序功能，则插入数据前必须关闭，否则插入新的数据会变乱
        if self.sorting:
            self.setSortingEnabled(False)
        # 如果设置了dataKey，则采用存量更新模式
        if self.dataKey:
            key = data[self.dataKey]
            # 如果键在数据字典中不存在，则先插入新的一行，并创建对应单元格
            if key not in self.dataDict:
                self.insertRow(updateRow)
                d = {}
                for n, header in enumerate(self.headerList):
                    content = data[header]
                    cellType = self.headerDict[header]['cellType']
                    cell = cellType(content)

                    if self.saveData:            # 如果设置了保存数据对象，则进行对象保存
                        cell.data = data

                    self.setItem(updateRow, n, cell)
                    d[header] = cell
                self.dataDict[key] = d
            # 否则如果已经存在，则直接更新相关单元格
            else:
                d = self.dataDict[key]
                for header in self.headerList:
                    content = data[header]
                    cell = d[header]
                    cell.setContent(content)

                    if self.saveData:            # 如果设置了保存数据对象，则进行对象保存
                        cell.data = data
        # 否则采用增量更新模式
        else:
            self.insertRow(updateRow)
            for n, header in enumerate(self.headerList):
                content = data[header]
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content)

                if self.saveData:
                    cell.data = data

                self.setItem(updateRow, n, cell)

        # 调整列宽
        if not self.columnResized:
            self.resizeColumns()
            self.columnResized = True

        # 重新打开排序
        if self.sorting:
            self.setSortingEnabled(True)
        # 设置行高
        self.setRowHeight(updateRow, 30)

    def onEvent(self, event):
        # dataframe转化方式>>> df.to_dict('records')
        # 数据格式[{'col1': 1.0, 'col2': 0.5}, {'col1': 2.0, 'col2': 0.75}]
        df = event.dict_['data']
        try:
            d = OrderedDict()
            self.removeRows()
            datalist = df.to_dict('records')
            fields = datalist[0].keys()
            for y in fields:
                d[y] = {"chinese": y, 'cellType': FrameCell}
            self.setHeaderDict(d)
            self.initTable()
            for x in datalist:
                self.updateData(x, lastRow=True)
        except Exception as e:
            self.mainEngine.writeLog(str(e))
        self.resizeColumnsToContents()

    def removeRows(self):
        while self.rowCount() > 0:
            self.removeRow(0)

    def update_by_list(self, datalist):
        try:
            d = OrderedDict()
            self.removeRows()
            fields = datalist[0].keys()
            for y in fields:
                d[y] = {"chinese": y, 'cellType': FrameCell}
            self.setHeaderDict(d)
            self.initTable()
            for x in datalist:
                self.updateData(x, lastRow=True)
        except Exception as e:
            raise e
            traceback.print_exc()

        self.resizeColumnsToContents()
