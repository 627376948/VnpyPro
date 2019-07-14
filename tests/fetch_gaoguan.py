import csv
import time

import pandas as pd
import tushare as ts


pro = ts.pro_api('2b66796cc972a3759369338cfb0dc2a908cfb3494dedd1f39a62b9e1')

# 获取stock_basic
stock_basic = pro.stock_basic(
    list_status='L', fields='ts_code, symbol, name, industry')
# 重命名行，便于后面导入neo4j
basic_rename = {'ts_code': 'TS代码', 'symbol': '股票代码',
                'name': '股票名称', 'industry': '行业'}
stock_basic.rename(columns=basic_rename, inplace=True)
# 保存为stock.csv
stock_basic.to_csv('stock.csv', encoding='utf-8')

# 获取top10_holders
holders = pd.DataFrame(columns=('ts_code', 'ann_date',
                                'end_date', 'holder_name', 'hold_amount', 'hold_ratio'))
# 获取一年内所有上市股票股东信息（可以获取一个报告期的）
for i in range(3610):
    code = stock_basic['TS代码'].values[i]
    top10_holders = pro.top10_holders(
        ts_code=code, start_date='20180101', end_date='20181231')
    holders = holders.append(top10_holders)
    time.sleep(0.3)  # 数据接口限制
# 保存为holders.csv
holders.to_csv('holders.csv', encoding='utf-8')

# 获取concept，并查看概念分类数量
concept = pro.concept()
concept.to_csv('concept_num.csv', encoding='utf-8')

# 获取concept_detail
concept_details = pd.DataFrame(
    columns=('id', 'concept_name', 'ts_code', 'name'))
for i in range(358):
    id = 'TS' + str(i)
    concept_detail = pro.concept_detail(id=id)
    concept_details = concept_details.append(concept_detail)
    time.sleep(0.3)
# 保存为concept_detail.csv
concept_details.to_csv('concept.csv', encoding='utf-8')
