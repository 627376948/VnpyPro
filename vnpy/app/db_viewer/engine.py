
from datetime import datetime
import csv

import pymongo

from vnpy.event import EventEngine
from vnpy.trader.engine import BaseEngine, MainEngine
from vnpy.trader.setting import SETTINGS


APP_NAME = "DbViewer"


class DbViewEngine(BaseEngine):
    """"""

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        """"""
        super().__init__(main_engine, event_engine, APP_NAME)
        self.username = SETTINGS["database.user"]
        self.password = SETTINGS["database.password"]
        self.host = SETTINGS["database.host"]
        self.port = SETTINGS["database.port"]
        self.authentication_source = SETTINGS["database.authentication_source"]
        try:
            self.db_client = pymongo.MongoClient(self.host, int(self.port))
            self.avtive = True
            self.update_db_info()
        except Exception as e:
            self.avtive = False

    def update_db_info(self):
        self.db_info = {
            "连接地址": self.db_client.HOST,
            "连接端口": str(self.db_client.PORT),
            "占用空间": str(self.db_client.server_info()['maxBsonObjectSize']),
            "连接状态": "连接中" if self.avtive else "断开连接"

        }
        self.dbs = self.db_client.list_database_names()

        for db in self.dbs:
            self.collections = {
                db: self.db_client[db].list_collection_names
            }

    def write_log(self, msg):
        print(msg)
        pass

    def get_db_names(self):
        return self.dbs

    def get_collections_by_dbname(self, db_name):
        return self.db_client[db_name].list_collection_names()

    def get_collection_info(self, db_name, collection_name):

        try:
            sample = self.db_client[db_name][collection_name].find_one()
        except Exception as e:
            self.write_log("无法获取sample")
            return []

        res = {
            "集合名称": collection_name,
            "所属数据库": db_name,
            "占用空间": f'{self.db_client[db_name].validate_collection(collection_name)["datasize"] / 1024 / 1024:.2f}M',
            "数据总量": str(self.db_client[db_name][collection_name].estimated_document_count())
        }
#         if "datetime" in sample.keys():
#             r = list(self.db_client[db_name][collection_name].find(
#                 sort=[("datetime", 1)], limit=1))
#             res["起始时间"] = str(r[0]["datetime"])
#             r = list(self.db_client[db_name][collection_name].find(
#                 sort=[("datetime", -1)], limit=1))
#             res["截至时间"] = str(r[0]["datetime"])
        self.collection_info = res
        return res

    def get_data(self, db_name, collection_name, flt={}, limit=100):
        try:
            d = list(self.db_client[db_name][collection_name].find(
                flt,
                {"_id": 0},
                limit=limit))
            return d
        except Exception as e:
            self.write_log(f"查到失败{db_name}.{collection_name}:{flt}")
            return []


if __name__ == '__main__':
    engine = DbViewEngine(None, None)
    engine.update_db_info()
    print(engine.get_db_names())
    print(engine.db_info["连接地址"])
    print(engine.db_info["连接端口"])
    print(engine.db_info["连接状态"])
    print(engine.db_info["占用空间"])
    for db in engine.get_db_names():
        for coll in engine.get_collections_by_dbname(db):
            print(f"{db}:{coll}")
    print(engine.get_data("quantaxis", "stock_min"))
    print(engine.get_collection_info("quantaxis", "stock_day"))

    info = [f"{k}:{v}" for k, v in engine.get_collection_info(
        "quantaxis", "stock_day").items()]
    print(info)
