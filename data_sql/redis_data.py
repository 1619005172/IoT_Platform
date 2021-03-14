# -*- coding: utf-8 -*- 
# @Time : 2021/1/7 9:35 
# @Author : kongbai 
# @File : redis_data.py
import redis
import config_py

from system_fun.error_code import error_sql


def redis_connect():
    try:
        pool = redis.ConnectionPool(host=config_py.r_host, port=config_py.r_port,
                                    password=config_py.r_passwd, decode_responses=True)
        # r = redis.Redis(host='localhost', port='6379', password='666666', decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        print(r)
        return r
    except:
        return error_sql.connect_error


# r.set('name', 'test')
# print(r['name'])
# print(r.get('name'))
# print(type(r.get('name')))


# 设备在线状态redis缓存
def online_state(device_mac, data):
    r = redis_connect()
    if r != error_sql.connect_error:
        r.set("online_%s" % device_mac, data)
        # print(r.get('PC_Test'))
        r.close()


def get_online(device_mac):
    r = redis_connect()
    try:
        if r != error_sql.connect_error:
            print('测试数据' + device_mac)
            print(r.mget(device_mac))
    except:
        print('查询出错')


def device_callback_set(mac, data):
    try:
        r = redis_connect()
        if r != error_sql.connect_error:
            r.set(mac, data)
            print('redis写入成功')
            r.close()
            # print(r.get(123456))
    except:
        print('redis写入失败')


def device_calback_get(mac):
    try:
        r = redis_connect()
        if r != error_sql.connect_error:
            data = r.get(mac)
            r.close()
            return data
    except:
        print('redis读取失败')


if __name__ == '__main__':
    device_callback(123456, 'success')
