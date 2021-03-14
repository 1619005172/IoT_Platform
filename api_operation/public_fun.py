# -*- coding: utf-8 -*- 
# @Time : 2021/1/6 13:10 
# @Author : kongbai 
# @File : public_fun.py


# 获取当前所有数据
import threading
import time
from threading import Thread

from threadpool import makeRequests

import config_py
from data_sql.mysql_data import get_data, get_data_fix
from data_sql.redis_data import device_calback_get, device_callback_set
from mqtt_operation.mqtt_connect import mqtt_publish
from system_fun.generate_tuple import generate_tuple, generate_history
from system_fun.error_code import err_user
from system_fun.json_analysis import generate_json


def api_get_all(key):
    data_token = get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % key)
    if data_token:
        # data = {}
        data1, data_list = get_data_fix("SELECT * FROM iot_device_bind")
        # column_name = get_data("SELECT COLUMN_NAME FROM information_schema.COLUMNS "
        #                        "WHERE TABLE_SCHEMA = 'flask_mqtt' AND TABLE_NAME = 'iot_device_bind'")
        # column_list = []
        # for i in data_list:
        #     column_list.append(i[0])
        # print(column_list)
        # j = 0
        # for row in data1:
        #     j += 1
        #     data2 = {}
        #     for i in range(len(column_list)):
        #         data2[column_list[i]] = row[i]
        #     data[j] = data2
        # print(data)
        data = generate_tuple(data_list, data1, 'bind')
        return data
    else:
        return err_user.authority


def api_get_type(key):
    data_token = get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % key)
    if data_token:
        data1, data_list = get_data_fix("SELECT * FROM iot_device_type")
        data = generate_tuple(data_list, data1, 'device')
        print(data)
        return data
    else:
        return err_user.key_error


def api_get_place(key):
    data_token = get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % key)
    if data_token:
        data1, data_list = get_data_fix("SELECT * FROM iot_device_place")
        data = generate_tuple(data_list, data1, 'place')
        print(data)
        return data
    else:
        return err_user.key_error


# 管理员、普通设备公用接口实现，获取所有设备类型名称
def api_get_all_typename(key):
    try:
        def data():
            data1, data_list = get_data_fix("SELECT * FROM iot_device_type")
            data2 = generate_tuple(data_list, data1, 'place')
            return data2

        if get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % key):
            data = data()
            # print('key' + str(data))
            return data
        elif get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % key):
            data = data()
            # print('token' + str(data))
            return data
        else:
            return err_user.key_error
    except:
        return err_user.error


# 管理员、普通设备公用接口实现，获取所有设备地址名称
def api_get_all_placename(key):
    try:
        def data():
            data1, data_list = get_data_fix("SELECT * FROM iot_device_place")
            data2 = generate_tuple(data_list, data1, 'place')
            return data2

        if get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % key):
            data = data()
            # print('key' + str(data))
            return data
        elif get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % key):
            data = data()
            # print('token' + str(data))
            return data
        else:
            print('用户验证失败')
            return err_user.key_error
    except:
        print('系统错误')
        return err_user.error


# 单个获取设备类型名称
def api_get_typename(key, type_id):
    try:
        def data(device_type_id):
            data1 = get_data("SELECT name FROM iot_device_type WHERE id = '%s'" % device_type_id)
            if data1:
                data3 = {'name': data1[0][0]}
                data2 = generate_json(data3)
                print(data2)
                return data2
            else:
                return err_user.empty

        if get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % key):
            data = data(type_id)
            # print('key' + str(data))
            return data
        elif get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % key):
            data = data(type_id)
            # print('token' + str(data))
            return data
        else:
            print('用户验证失败')
            return err_user.key_error
    except:
        print('系统错误')
        return err_user.error


# 单个获取设备地址名称
def api_get_placename(key, place_id):
    try:
        def data(device_place_id):
            data1 = get_data("SELECT name FROM iot_device_place WHERE id = '%s'" % device_place_id)
            if data1:
                data3 = {'name': data1[0][0]}
                data2 = generate_json(data3)
                print(data2)
                return data2
            else:
                return err_user.empty

        if get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % key):
            data = data(place_id)
            # print('key' + str(data))
            return data
        elif get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % key):
            data = data(place_id)
            # print('token' + str(data))
            return data
        else:
            print('用户验证失败')
            return err_user.key_error
    except:
        print('系统错误')
        return err_user.error


# 获取指定设备所有历史记录
def api_get_mqtt_allhistory(key, bind_id):
    try:
        def data(bindid):
            data1, data_list = get_data_fix("SELECT * FROM iot_mqtt_historical WHERE bind_id = '%s'" % bindid)
            data2 = generate_tuple(data_list, data1, 'bind')
            return data2

        if get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % key):
            data = data(bind_id)
            print('key' + str(data))
            return data
        elif get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % key):
            data = data(bind_id)
            print('token' + str(data))
            return data
        else:
            print('用户验证失败')
            return err_user.key_error
    except:
        print('系统错误')


# 指定设备历史消息条数与分页数
def api_get_mqtt_numhistory(key, bind_id):
    try:
        # data_token = get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % key)
        def mqtt_num_pag(bindid):
            bind_id = bindid
            num = get_data("SELECT COUNT(bind_id) FROM iot_mqtt_historical WHERE bind_id = '%s'" % bind_id)[0][0]
            if num <= 10 & num > 0:
                pag = 1
            else:
                pag_integer = num // 10
                # print(pag_integer)
                if num - pag_integer == 0:
                    pag = pag_integer
                else:
                    pag = pag_integer + 1
            # print(pag)
            # print(pag_decimal)
            data = generate_history(num, pag)
            data1 = generate_json(data)
            print(data1)
            return data1

        if get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % key):
            data = mqtt_num_pag(bind_id)
            return data
        elif get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % key):
            data = mqtt_num_pag(bind_id)
            return data

        else:
            print('用户验证失败')
            return err_user.key_error
    except:
        print('系统错误')


# 指定设备历史消息分页查询
def api_get_mqtt_paghistory(key, bind_id, pag):
    pag = int(pag)
    # print("方法内"+bind_id,pag)
    try:
        def data(bindid, pag):
            args = (bindid, pag)
            data1, data_list = get_data_fix(
                "SELECT * FROM iot_mqtt_historical WHERE bind_id = '%s'limit %s,10 " % args)
            data2 = generate_tuple(data_list, data1, 'bind')
            return data2

        # data_token = get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % key)
        if get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % key):
            if pag == 1:
                pag = 0
            else:
                pag = pag * 10 - 10
            data = data(bind_id, pag)
            print(data)
            return data
        elif get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % key):
            if pag == 1:
                pag = 0
            else:
                pag = pag * 10 - 10
            data = data(bind_id, pag)
            print(data)
            return data
        else:
            print('用户验证失败')
            return err_user.key_error
    except:
        print('系统错误')


i = True
callback_data = ''


# 设备控制
def user_device_ctrl(key, mac, instruction_id):
    # 控制函数
    def ctrl(mac, instruction_id):
        instruction = get_data("SELECT data FROM iot_control_bind WHERE type_id = '%s'" % instruction_id)
        # print(instruction[0][0])
        data = {}
        data.update({'mac': mac})
        data.update({'data': instruction[0][0]})
        print(data)
        ctrl_send_mqtt = mqtt_publish(generate_json(data))
        if ctrl_send_mqtt == 'PUBLISH_SUCCESS':
            print('线程开启之前' + str(i))
            thrding_start()
            return huidiaojiance(mac)
        else:
            print('error')
            return 'error'

    # ctrl(mac, instruction_id)
    if get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % key):
        data = ctrl(mac, instruction_id)
        return data
    elif get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % key):
        data = ctrl(mac, instruction_id)
        return data


class time_threading(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self) -> None:
        time_time()


class mqtt_threading(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self) -> None:
        huidiaojiance()


def thrding_start():
    thread_1 = time_threading(1, "time_thread", 1)
    # thread_2 = mqtt_threading(1, "mqtt_thread", 1)
    thread_1.start()
    # thread_2.start()


# 响应超时计时函数
def time_time():
    print('阻塞计时线程启动')
    global i
    while True:
        time.sleep(3)
        break
    i = False


def huidiaojiance(mac):
    data = 'error'
    j = 0
    global i
    i = True
    print('循环线程启动')
    while i:
        # j = j + 1
        # print(j)
        print(config_py.mqtt_msg)
        re = device_calback_get(mac)
        if re == 'success':
            data = re
            device_callback_set(mac, 'None')
            print('success')
            # global callback_data
            # callback_data = data
            return data
            # break
    # callback_data = data
    print(data)
    return data


# # 开启、关闭指定设备
# def api_tactics_on_off(key, mac, msg):
#     try:
#
#         if get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % key):
#             # data = data(place_id)
#             # print('key' + str(data))
#             return
#         elif get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % key):
#             # data = data(place_id)
#             # print('token' + str(data))
#             return
#         else:
#             print('用户验证失败')
#             return err_user.key_error
#
#     except:
#         print('系统错误')


if __name__ == '__main__':
    device_ctrl('6938EC5F52BECAE00F583E4F02D056D8', 8053921, 1)
