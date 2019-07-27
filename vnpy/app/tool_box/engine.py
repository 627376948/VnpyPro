# encoding: UTF-8

'''
桌面工具引擎，提供各类辅助功能
'''
from collections import OrderedDict
from queue import Queue
from threading import Thread
import json
import os
import re
import traceback

import xlrd
import xlwt

from vnpy.app.tool_box.util import (get_jsonpath,
                                    get_filelist,
                                    strfint,
                                    strftime,
                                    un_zip_files,
                                    get_new_name)
from vnpy.trader.engine import BaseEngine, MainEngine


APP_NAME = "ToolBox"

CHINESE = {
    "do_search": "查询文件工具",
    "filename": "查询关键字",
    "dir_path": "目录所在路径",
    "do_compact_xls": "XLS合并工具",
    "headline": "文件标题占用行数",
    "tailline": "文件结尾占用行数",
    "do_split_xls": "XLS拆分工具",
    "n_perfile": "每个拆分文件行数",
    "file_path": "文件所在路径",
    "do_upzip": "指令解压工具",
    "files_type": "指令所属类型"
}


class ToolBoxEngine(BaseEngine):
    """工具箱引擎"""

    settingFileName = 'tool_setting.json'
    setting_file_path = get_jsonpath(settingFileName, __file__)

    def __init__(self, mainEngine, eventEngine):
        """Constructor"""
        super().__init__(mainEngine, eventEngine, APP_NAME)
        self.mainEngine = mainEngine
        self.eventEngine = eventEngine
        # 文件查询相关
        self.keywords = []  # 待查询的字符串集合
        self.result_list = []  # 查询结果
        self.files = []  # 待匹配的文件集合
        # Xls文件信息查询相关
        self.xls_file = {}
        self.xls_parser = XlsParser()
        # 负责执行数据库插入的单独线程相关
        self.active = False  # 工作状态
        self.queue = Queue()  # 队列
        self.thread = Thread(target=self._run)  # 线程

        # 载入设置
        self.setting = {}
        self.load_setting()
        # 注册事件监听
        self.register_event()

    def load_setting(self):
        """加载配置"""
        with open(self.setting_file_path) as f:
            self.setting = json.load(f)
        return self.setting

    def save_setting(self, dict=None):
        """储存配置"""
        with open(self.setting_file_path, 'w') as f:
            if dict:
                self.setting.update(dict)
            content = json.dumps(self.setting)
            f.write(content)

    def get_setting(self):
        """获取配置"""
        return self.setting

    def register_event(self):
        """注册事件监听"""
        pass

    def _run(self):
        """运行app线程"""
        while self.active:
            try:
                pass
            except Exception as e:
                pass

    def start(self):
        """启动"""
        self.active = True
        self.thread.start()

    def stop(self):
        """退出"""
        if self.active:
            self.active = False
            self.thread.join()

    def find_files(self, root: str=None):
        """"""
        if root:
            self.root = root
        self.files = []
        for root, dirs, files in os.walk(self.root, topdown=True):
            for name in files:
                self.files.append([name, os.path.join(root, name)])
        return self.files

    def traverse_files(self, keywords: list):
        """遍历文件，匹配字符串"""
        self.result_list = []
        self.keywords = keywords

        for file_name, file_path in self.files:
            for item2 in self.keywords:
                if item2:
                    # 正则匹配，不区分大小写
                    searchObj = re.search(
                        r'(.*)' + item2 + '.*', file_name, re.M | re.I)
                    if searchObj:
                        d = OrderedDict()
                        d["文件名称"] = file_name
                        d["文件路径"] = file_path
                        d["文件大小"] = strfint(os.path.getsize(file_path))
                        d["更新时间"] = strftime(os.path.getmtime(file_path))
                        self.result_list.append(d)
                    else:
                        pass
        return self.result_list

    def clear_xls(self, xls_files: str, col_name: str="企业内部员工编号"):
        """"""
        try:
            for xls_file in xls_files:
                cur_xls = xlrd.open_workbook(xls_file)
                cur_sheet = cur_xls.sheet_by_index(0)
                save_file = xlwt.Workbook()
                save_sheet = save_file.add_sheet("sheet1")
                for col in range(cur_sheet.ncols):
                    for row in range(cur_sheet.nrows):
                        if cur_sheet.cell(0, col).value == col_name:
                            save_sheet.write(0, col, col_name)
                            break
                        else:
                            save_sheet.write(row,
                                             col,
                                             cur_sheet.cell(row, col).value)
                save_file.save(xls_file)
            return "清洗xls完成"
        except Exception as e:
            return "清洗报错:{}".format(str(e))

    def compact_xls(
            self,
            file_name: str,
            load_path: str,
            save_path: str,
            headline: int=1,
            tailline: int=0):
        """合并xls"""
        if load_path:
            pass
        else:
            raise Exception(f"选择的路径不正确{load_path}")

        file_list = get_filelist(load_path)
        tofile = os.path.join(save_path, file_name)
        ret_book = xlwt.Workbook()
        ret_sheet = ret_book.add_sheet('sheet1')
        x, y, startrow = 0, 0, 0
        self.result_list = []
        for file_ in file_list:
            workbook = xlrd.open_workbook(os.path.join(load_path, file_))
            sheet = workbook.sheet_by_index(0)
            nrows = sheet.nrows
            ncols = sheet.ncols
            for i in range(startrow, nrows - tailline):
                for j in range(0, ncols):
                    try:
                        ret_sheet.write(x, y, sheet.cell(i, j).value)
                        y += 1
                    except Exception as e:
                        print(e)
                        print("合成xls时发生问题")
                x += 1
                y = 0
            startrow = headline
        ret_book.save(tofile)
        d = OrderedDict()
        d["文件名称"] = file_name
        d["文件路径"] = os.path.abspath(tofile)
        d["文件大小"] = strfint(os.path.getsize(tofile))
        d["更新时间"] = strftime(os.path.getmtime(tofile))
        self.result_list.append(d)
        return self.result_list

    def split_xls(
            self,
            src_file: str,
            save_path: str,
            headline: int=1,
            n_perfile: int=100):
        """"拆分xls"""
        if src_file:
            pass
        else:
            raise Exception(f"选择的路径不正确{src_file}")

        workbook = xlrd.open_workbook(filename=src_file)
        sheet = workbook.sheet_by_index(0)
        nrows, ncols = sheet.nrows, sheet.ncols
        i = headline  # 原始文件游标
        self.result_list = []

        while i in range(nrows):
            j = 0  # 每个切分文件的游标
            start_i = i + 1
            ret_book = xlwt.Workbook()
            ret_sheet = ret_book.add_sheet('sheet1')
            for j in range(headline):  # 写表头
                k = 0
                for k in range(ncols):  # 一列一列写入表头
                    ret_sheet.write(j, k, sheet.cell(j, k).value)
                    k += 1
                j += 1

            for j in range(headline, headline + n_perfile):  # 写入内容
                k = 0
                if(i >= nrows):  # 大于源文件总行数则调出循环
                    break
                for k in range(ncols):  # 一列一列写入内容
                    ret_sheet.write(j, k, sheet.cell(i, k).value)
                    k += 1
                i += 1

            name = 'cutfile{}-{}.xls'.format(start_i, i)
            tofile = os.path.join(save_path, name)
            ret_book.save(tofile)
            d = OrderedDict()
            d["文件名称"] = name
            d["文件路径"] = os.path.abspath(tofile)
            d["文件大小"] = strfint(os.path.getsize(tofile))
            d["更新时间"] = strftime(os.path.getmtime(tofile))
            self.result_list.append(d)
        return self.result_list

    def get_xls_tables(self):
        """获取数据表"""
        return list(self.xls_file.keys())

    def get_xls_col_names(self, table_name: str):
        """获取xls字段"""
        df = pd.read_excel(self.xls_file[table_name], sheet_name=0)
        return df.columns.values.tolist()

    def qry_xls_info(
            self,
            keywords: str="",
            table_name: str="联系人表",
            col_name: str="联系人姓名"):
        """查询xls指定信息"""
        df = pd.read_excel(self.xls_file[table_name], sheet_name=0)
        df = df[df[col_name].notna()]
        df = df[df[col_name].str.contains(keywords)] if keywords else df
        df = df.fillna("-")
        self.result_list = df.to_dict(orient="records")
        return self.result_list

    def upzip_dir(self, rootdir: str):
        """解压缩目录下所有文件"""
        if rootdir:
            un_zip_files(rootdir)
        else:
            raise Exception(f"选择的路径不正确{rootdir}")

    def parser_xls(
            self,
            xls_files: list,
            xls_type: str):
        """解析xls"""
        self.result_list = []
        for file in xls_files:
            if ".xls" in os.path.basename(file):
                d = self.xls_parser.parser(file, xls_type)
                if d:
                    self.result_list.append(d)
        return self.result_list

    def do_search(self,
                  filename: str="",
                  dir_path: str=""
                  ):
        """执行查找"""
        try:
            files = self.find_files(dir_path)
            if files:
                resluts = self.traverse_files([filename])
                return [True, resluts]
            else:
                return [False, f"在{dir_path}没有找到相关文件{filename}"]
        except Exception as e:
            return [False, f"报错了{str(e)}"]

    def do_compact_xls(self,
                       headline: int=1,
                       tailline: int=0,
                       dir_path: str=""):
        """执行合并xls"""

        try:
            resluts = self.compact_xls("合并结果.xls",
                                       dir_path,
                                       dir_path,
                                       headline,
                                       tailline)
            return [True, resluts]
        except Exception as e:
            return [False, str(e)]

    def do_split_xls(self,
                     headline: int=1,
                     n_perfile: int=1500,
                     file_path: str=""):
        """执行拆分xls"""
        try:
            resluts = self.split_xls(file_path,
                                     os.path.dirname(file_path),
                                     headline,
                                     n_perfile)
            return [True, resluts]
        except Exception as e:
            return [False, str(e)]

    def do_upzip(self,
                 files_type: str="平安",
                 dir_path: str=""):
        """解压缩，files_type为平安或者国寿"""
        try:
            self.upzip_dir(dir_path)
            files = self.find_files(dir_path)
            if files:
                xls_files = self.traverse_files([".xls"])
                xls_files = [x["文件路径"] for x in xls_files]
                resluts = self.parser_xls(xls_files, files_type)
                return [True, resluts]
            else:
                return [False, f"解压后没有找到文件"]
        except Exception as e:
            return [False, str(e)]
            traceback.print_exc()


class XlsParser():
    """Xls解析器，用于解析受托（平安和国寿）的xls指令"""

    def __init__(self, path=None, xls_type="平安"):
        self.path = path
        self.xls_type = xls_type

    def parser(self, path=None, xls_type=None):
        self.path = path if path else self.path
        self.xls_type = xls_type if xls_type else self.xls_type
        try:
            self.cur_sheet = xlrd.open_workbook(self.path).sheet_by_index(0)
        except Exception as e:
            self.cur_sheet = None
            print(f"发现一个格式有问题，无法打开的xls:{self.path}\n{str(e)}")

        self.ret_dict = OrderedDict()
        self.ret_dict["业务类型"] = self.get_order_type()
        self.ret_dict["指令位置"] = os.path.abspath(self.path)
        self.ret_dict["企业名称"] = self.get_com_name()
        self.ret_dict["人数条数"] = self.get_size()
        self.ret_dict["缴费开始日期"] = self.get_start_date()
        self.ret_dict["缴费结束日期"] = self.get_end_date()
        self.ret_dict["公共账户缴费"] = self.get_gg_jf()
        self.ret_dict["公共账户类型"] = self.get_gg_type()
        self.ret_dict["总缴费"] = self.get_sum_jf()
        self.ret_dict["是否已处理"] = "No"
        self.ret_dict["报错原因"] = ""
        self.ret_dict["报错指令位置"] = ""
        self.ret_dict["指令日期"] = ""
        return self.ret_dict

    def get_com_name(self):
        if self.xls_type == "平安":
            if self.path.split(os.path.sep)[-3] == "暂停":
                return self.path.split(os.path.sep)[-4]
            else:
                return self.path.split(os.path.sep)[-3]
        if self.xls_type == "国寿":
            return os.path.basename(self.path)

    def get_order_type(self):
        if self.xls_type == "平安":
            basename = os.path.basename(self.path)
            dirname = self.path.split(os.path.sep)[-2]
            print(self.path)
            if "个人信息变更" in basename and dirname == "待遇支付":
                return f"2.{dirname}_个人信息变更"
            elif "个人信息变更" in dirname:
                return f"2.{dirname}"
            elif "调账" in dirname:
                return f"11.{dirname}"
            elif "待遇支付" in dirname:
                return f"7.{dirname}"
            elif "受益人" in os.path.basename(self.path):
                return f"10.受益人信息变更"
            elif "保留" in dirname or "恢复" in dirname:
                return f"6.{dirname}"

        if self.xls_type == "国寿":
            if "人员信息修改" in os.path.basename(self.path):
                # 人员信息修改
                return "2.人员信息修改"

            elif "支付申请登记" in os.path.basename(self.path):
                # 人员信息修改
                return "7.支付申请登记"

            elif "公共账户缴费" in os.path.basename(self.path):
                return "4.公共账户缴费"

            elif "缴费通知单" in os.path.basename(self.path):
                return "4.到账通知单"

            elif "缴费申请汇总表" in os.path.basename(self.path):
                # 缴费指令
                return "4.缴费汇总表"

            if self.cur_sheet:
                if self.cur_sheet.cell(0, 5).value == "缴费来源*":
                    # 缴费指令
                    return "4.缴费"

                elif self.cur_sheet.cell(0, 4).value == "性别*":
                    # 缴费指令
                    return "1.新增"

                elif self.cur_sheet.cell(1, 4).value == "转保留" or \
                        self.cur_sheet.cell(1, 4).value == "计划内集团内" or \
                        self.cur_sheet.cell(1, 4).value == "计划外":
                    # 转移指令
                    return f"3.{self.cur_sheet.cell(1,4).value}"

                elif self.cur_sheet.cell(0, 5).value == "修改字段名*":
                    return "2.人员信息修改"
            else:
                return "9.非标准指令"

    def get_size(self):
        return self.cur_sheet.nrows - 1 if self.cur_sheet else 0

    def get_start_date(self):
        if self.get_order_type() == "4.缴费":
            if self.xls_type == "国寿":
                sheet = xlrd.open_workbook(get_new_name(
                    self.path, "_企业年金缴费申请汇总表", False)).sheet_by_index(0)
                return sheet.cell(5, 3).value
        else:
            return ""

    def get_end_date(self):
        if self.get_order_type() == "4.缴费":
            if self.xls_type == "国寿":
                sheet = xlrd.open_workbook(get_new_name(
                    self.path, "_企业年金缴费申请汇总表", False)).sheet_by_index(0)
                return sheet.cell(5, 4).value
        else:
            return ""

    def get_gg_jf(self):
        if self.get_order_type() == "4.缴费":
            if self.xls_type == "国寿":
                filename = os.path.join(
                    os.path.dirname(self.path), "公共账户缴费.xls")
                if os.path.exists(filename):
                    book = xlrd.open_workbook(filename)
                    sheet = book.sheet_by_index(0)
                    return sheet.cell(1, 2).value
                else:
                    return""
        else:
            return ""

    def get_gg_type(self):
        if self.get_order_type() == "4.缴费":
            if self.xls_type == "国寿":
                filename = os.path.join(
                    os.path.dirname(self.path), "公共账户缴费.xls")
                if os.path.exists(filename):
                    book = xlrd.open_workbook(filename)
                    sheet = book.sheet_by_index(0)
                    return sheet.cell(1, 1).value
                else:
                    return""
        else:
            return ""

    def get_sum_jf(self):
        if self.get_order_type() == "4.缴费":
            if self.xls_type == "国寿":
                sheet = xlrd.open_workbook(get_new_name(
                    self.path, "_企业年金缴费申请汇总表", False)).sheet_by_index(0)
                return sheet.cell(5, 13).value
        else:
            return ""


if __name__ == "__main__":
    tb = ToolBoxEngine(None, None)
    msg, res = tb.do_search(r"C:\Users\Thinkpad\Desktop\杂项", "h")
    from pprint import pprint
    pprint(res)
