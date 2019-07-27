# coding:UTF-8
"""

"""
from queue import Queue
import datetime
import os
import time
import zipfile


def get_filelist(rootdir='.\\', type_='File'):
    '''参数为指明被遍历的文件夹,默认遍历文件，type为其他时遍历目录'''
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        if type_ == 'File':
            return filenames  # 输出文件名列表信息
        elif type_ == 'Folder':
            return dirnames
        elif type_ == 'Parent':
            return parent


def get_date_today():
    """获取当前本机电脑时间的日期"""
    return datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


jsonPathDict = {}


def get_jsonpath(name, moduleFile):
    """
    获取JSON配置文件的路径：
    1. 优先从当前工作目录查找JSON文件
    2. 若无法找到则前往模块所在目录查找
    """
    currentFolder = os.getcwd()
    currentJsonPath = os.path.join(currentFolder, name)
    if os.path.isfile(currentJsonPath):
        jsonPathDict[name] = currentJsonPath
        return currentJsonPath

    moduleFolder = os.path.abspath(os.path.dirname(moduleFile))
    moduleJsonPath = os.path.join(moduleFolder, '.', name)
    jsonPathDict[name] = moduleJsonPath
    return moduleJsonPath


def strfint(fsize_int):
    return str("{:.2f}m".format(fsize_int / 1024 / 1024))


def strftime(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))


def cp437_to_utf8(strs):
    try:
        new_str = strs.encode('cp437')
        new_str = new_str.decode("gbk")
        return new_str
    except Exception as e:
        return strs


def inc_num(max_num):
    for i in range(max_num):
        yield str(i)


def inc_name(max_num, key="name"):
    for i in range(max_num):
        yield f"{key}{str(i)}"


inc_number = inc_num(999999)
inc_name = inc_name(999999)


def get_new_name(src_name, add_name="_新", is_random=True):
    if is_random:
        random_str = inc_number.__next__()
        return os.path.join(os.path.dirname(src_name),
                            "{}{}{}.{}".format(os.path.basename(src_name).split(".")[0],
                                               add_name,
                                               random_str,
                                               os.path.basename(
                                                   src_name).split(".")[1]
                                               )
                            )
    else:
        return os.path.join(os.path.dirname(src_name),
                            "{}{}.{}".format(os.path.basename(src_name).split(".")[0],
                                             add_name,
                                             os.path.basename(
                                                 src_name).split(".")[1]
                                             )
                            )


def un_zip(file_name, file_type=(".xls", ".xlsx", ".pdf")):
    sub_zip_files = []
    un_zip_files = []
    dirname = os.path.dirname(file_name)
    with zipfile.ZipFile(file_name) as zip_file:
        for x in zip_file.namelist():
            new_file_name = os.path.abspath(os.path.join(dirname, x))
            utf8_name = os.path.abspath(
                os.path.join(dirname, cp437_to_utf8(x)))
            basename = os.path.basename(utf8_name)
            if basename.endswith(".zip"):
                zip_file.extract(x, cp437_to_utf8(dirname))
                # 重命名文件
                if os.path.exists(utf8_name):
                    utf8_name = get_new_name(utf8_name)
                os.rename(new_file_name, utf8_name)
                # 目标清单中增加一个
                sub_zip_files.append(utf8_name)
            # 解压缩指定文件扩展名的文件
            if os.path.splitext(utf8_name)[1] in file_type:
                zip_file.extract(x, cp437_to_utf8(dirname))
                # 重命名文件
                if os.path.exists(utf8_name):
                    utf8_name = get_new_name(utf8_name)
                os.rename(new_file_name, utf8_name)
                un_zip_files.append(utf8_name)

    return un_zip_files, sub_zip_files


def un_zip_files(rootdir="C:\\Users\\bjfh-chenjy\\Desktop\\13日\\"):
    target_queue = Queue()
    # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent, dirnames, filenames in os.walk(rootdir):
        for file in filenames:
            if file.endswith(".zip"):
                target_queue.put(os.path.join(parent, file))

    while target_queue.qsize() != 0:
        file_name = target_queue.get()
        un_zip_files, sub_zip_files = un_zip(file_name)
        for zip_file in sub_zip_files:
            target_queue.put(zip_file)


if __name__ == "__main__":
    #     un_zip_files(rootdir = "C:\\Users\\bjfh-chenjy\\Desktop\\18日\\第二批")
    #     path = "C:\\Users\\bjfh-chenjy\\Desktop\\测试\\中国移动通信集团广西有限公司_20190218094551\\待遇支付\\个人信息变更申请批量表.xls"
    #     print(
    #         get_new_name(path)
    #         )
    print(inc_name.__next__())
    print(inc_number.__next__())
    print(inc_number.__next__())
