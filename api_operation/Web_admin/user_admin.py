# -*- coding: utf-8 -*- 
# @Time : 2020/12/24 19:40 
# @Author : kongbai 
# @File : user_admin.py
# 管理员接口处理部分

from system_fun.encryption_method import blend_pw, md5_pas1, sha256_pas2
from data_sql.mysql_data import get_data, sql_updata, del_data, get_data_fix
from system_fun.generate_tuple import generate_tuple, generate_online
from system_fun.get_date import get_time
from system_fun.token_gen import token_gen
from system_fun.sql_data_cache import device_bind, device_type, device_place
from system_fun.error_code import err_user, error_sql


# 登录验证
def login(username, password):
    text = blend_pw(md5_pas1(password), sha256_pas2(password))
    args = username
    data = get_data("SELECT password FROM iot_user_admin WHERE username = '%s'" % args)
    if data:
        passwd = data[0][0]
        print(data)
        if text == passwd:
            token = token_gen()
            sql_updata("UPDATE iot_user_admin SET token = '%s' WHERE username = '%s'" % (token, args))
            return err_user.success, token
        else:
            return err_user.error, err_user.empty
    else:
        return err_user.no_user, err_user.empty


# 添加管理员
def add_admin(username, password, token, mail, phone):
    text = blend_pw(md5_pas1(password), sha256_pas2(password))
    args = (username, text, mail, phone)
    username_data = get_data("SELECT * FROM iot_user_admin WHERE username = '%s'" % args[0])
    data_token = get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % token)
    print(data_token)
    if data_token:
        if username_data:
            return err_user.user_already
        else:
            return sql_updata(
                "INSERT INTO iot_user_admin (username,password,mail,phone) "
                "VALUES ('%s','%s','%s','%s')" % args)
    else:
        return err_user.authority


# 删除管理员
def del_admin(user_id, token):
    args = user_id
    username_data = get_data("SELECT * FROM iot_user_admin WHERE id = '%s'" % args)
    data_token = get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % token)
    if data_token:
        if username_data:
            print('开始删除')
            del_data("DELETE FROM iot_user_admin WHERE id = '%s'" % args)
            return err_user.success
        else:
            return err_user.no_user
    else:
        return err_user.authority


# 获取当前所有绑定数据
def get_data_sql(token):
    data_token = get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % token)
    if data_token:
        data1, data_list = get_data_fix("SELECT * FROM iot_device_bind")
        # data1, data_list = get_data_fix(
        #     "select iot_device_bind.*,"
        #     "iot_control_bind.type_id,"
        #     "iot_control_bind.`ctrl_name`,"
        #     "iot_control_bind.`data` "
        #     "from iot_device_bind "
        #     "left join iot_control_bind "
        #     "on iot_device_bind.mac=iot_control_bind.mac")
        # data_list = []
        # ctrl_list = []
        # all_list = []
        # for i in data_list:
        #     all_list.append(i[0])
        # print(all_list)
        # for j in all_list:

            # print(sql_data1)
        # print(data1)
        data = generate_tuple(data_list, data1, 'bind')
        return data
    else:
        return err_user.authority


# 获取绑定设备在线数量
def get_online_all(token):
    data_token = get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % token)
    if data_token:
        try:
            num = get_data("SELECT COUNT(online) FROM iot_device_bind WHERE online = '1'")
            data = generate_online(num[0][0])
            print(data)
            return data
        except:
            return error_sql.error
        # print(data1)
    else:
        return err_user.authority


# 添加设备类型
def add_type(token, type, name):
    try:
        data_token = get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % token)
        if data_token:
            # print(data_token[0][0])
            user_id = data_token[0][0]
            args = (type, name, get_time(), user_id)
            data_type = get_data("SELECT * FROM iot_device_type WHERE type = '%s'" % args[0])
            if data_type:
                print(err_user.user_already)
                return err_user.user_already
            else:
                # print(data_type)
                data = sql_updata("INSERT INTO iot_device_type (type ,name ,date ,user_id) "
                                  "VALUES ('%s','%s','%s','%s')" % args)
                return data
        else:
            return err_user.authority
    except:
        return err_user.authority


# 添加设备地址
def add_place(token, type, name):
    try:
        data_token = get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % token)
        if data_token:
            # print(data_token[0][0])
            user_id = data_token[0][0]
            args = (type, name, get_time(), user_id)
            data_place = get_data("SELECT * FROM iot_device_place WHERE type = '%s'" % args[0])
            if data_place:
                print(err_user.user_already)
                return err_user.user_already
            else:
                # print(data_type)
                data = sql_updata("INSERT INTO iot_device_place (type ,name ,date ,user_id) "
                                  "VALUES ('%s','%s','%s','%s')" % args)
                return data
        else:
            return err_user.authority
    except:
        return err_user.authority


# 获取设备类型
def get_type(token):
    data_token = get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % token)
    if data_token:
        data1, data_list = get_data_fix("SELECT * FROM iot_device_type")
        data = generate_tuple(data_list, data1, 'device')
        print(data)
        return data
    return err_user.authority


# 获取设备地址
def get_place(token):
    data_token = get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % token)
    if data_token:
        data1, data_list = get_data_fix("SELECT * FROM iot_device_place")
        data = generate_tuple(data_list, data1, 'place')
        print(data)
        return data
    else:
        return err_user.authority


# 添加设备
def add_device_bind(token, device_id, place_id, name, device_mac):
    data_token = get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % token)
    if data_token:
        time = get_time()
        args = (device_id, place_id, name, device_mac, time)
        data_mac = get_data("SELECT * FROM iot_device_bind WHERE mac = '%s'" % args[3])
        print(data_mac)
        if data_mac:
            return '此设备已绑定'
        else:
            data = sql_updata("INSERT INTO iot_device_bind(device_id,place_id,name,mac,date)"
                              "VALUES ('%s','%s','%s','%s','%s')" % args)
            return data
            print(data)
    else:
        return err_user.authority


# 删除设备
def del_device_bind(token, device_id):
    data_token = get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % token)
    if data_token:
        try:
            return del_data("DELETE FROM iot_device_bind WHERE id = '%s'" % device_id)
        except:
            error_sql.error
    else:
        return err_user.authority


# 管理员添加控制类型
def user_add_ctrl_type(token, type_id, name):
    data_token = get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % token)
    if data_token:
        user_id = data_token[0][0]
        time = get_time()
        args = (type_id, name, time, user_id)
        data_type = get_data("SELECT * FROM iot_control_type WHERE type = '%s'" % args[0])
        # print(data_type)
        if data_type:
            return '此类型已添加'
        else:
            data = sql_updata("INSERT INTO iot_control_type(type,name,date,user_id)"
                              "VALUES ('%s','%s','%s','%s')" % args)
            return data
    else:
        return err_user.authority


# 管理员获取所有控制类型
def user_get_ctrl_type(token):
    data_token = get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % token)
    if data_token:
        data_type, data_list = get_data_fix("SELECT * FROM iot_control_type")
        data = generate_tuple(data_list, data_type, 'place')
        return data
    else:
        return err_user.authority


# 管理员绑定控制指令
def bind_ctrl_dir(token, type_id, mac, name, data):
    data_token = get_data("SELECT * FROM iot_user_admin WHERE token = '%s'" % token)
    args = (type_id, mac, name, data)
    if data_token:
        data_name = get_data("SELECT * FROM iot_control_bind WHERE ctrl_name = '%s'" % args[2])
        if data_name:
            return '此指令已添加'
        else:
            time = get_time()
            user_id = data_token[0][0]
            args2 = (time, user_id)
            args = args + args2
            data = sql_updata("INSERT INTO iot_control_bind(type_id,device_bind_id,ctrl_name,data,date,user_id)"
                              "VALUES ('%s','%s','%s','%s','%s','%s')" % args)
            return data
    else:
        return err_user.authority


if __name__ == '__main__':
    add_type('b5cc478c70e7831405dd000f87b541f0', 3, '测试类型2')
