# -*- coding: utf-8 -*- 
# @Time : 2021/1/6 17:27 
# @Author : kongbai 
# @File : generate_tuple.py

# 数据库数据生成元组
from data_sql.redis_data import get_online


def generate_tuple(data_list, data, name):
    data1 = []
    column_list = []
    for i in data_list:
        column_list.append(i[0])
    print(column_list)
    for row in data:
        data2 = {}
        for i in range(len(column_list)):
            data2[column_list[i]] = str(row[i])
        data1.append(data2)
    return data1


# # 在线数据处理(已作废)
# def generate_online(mac_data):
#     data = []
#     for row in mac_data:
#         text = list(row)
#         print(text)
#         data.append(get_online(text))
#     return data

# 在线数据处理
def generate_online(num):
    num = str(num)
    data = [{'online': num}]
    return data


# 设备历史数据处理
def generate_history(num, pag):
    data = {'all': num, 'pag': pag}
    return data
