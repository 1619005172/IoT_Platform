# -*- coding: utf-8 -*- 
# @Time : 2020/12/24 19:31 
# @Author : kongbai 
# @File : mysql_data.py
# 数据库数据处理
import pymysql
import config_py
from system_fun.error_code import error_sql


# 连接数据库
# 失败返回Error
def db_connect():
    try:
        db = pymysql.connect(config_py.db_url,
                             config_py.db_user,
                             config_py.db_passwd,
                             config_py.db_from)
        cursor = db.cursor()
        re = db, cursor
        return re
    except:
        return error_sql.connect_error


# 查询数据库
# sql为mysql语句
# 返回查询结果
def get_data(sql):
    if db_connect() != error_sql.connect_error:
        db, cursor = db_connect()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            fields = cursor.description
            return results
        except:
            return error_sql.error
        db.close()
    else:
        return error_sql.connect_error


# 修正版获取
def get_data_fix(sql):
    if db_connect() != error_sql.connect_error:
        db, cursor = db_connect()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            fields = cursor.description
            return results, fields
        except:
            return error_sql.error
        db.close()
    else:
        return error_sql.connect_error


# # 修正版获取
# def get_data_fix2(sql):
#     if db_connect() != error_sql.connect_error:
#         db, cursor = db_connect()
#         try:
#             cursor.execute(sql)
#             results = cursor.fetchall()
#             fields = cursor.description
#             rowcount = cursor.rowcount
#             return results, fields
#         except:
#             return error_sql.error
#         db.close()
#     else:
#         return error_sql.connect_error


# 插入/更新数据库
# sql为mysql语句
def sql_updata(updata_sql):
    if db_connect() != error_sql.connect_error:
        db, cursor = db_connect()
        try:
            cursor.execute(updata_sql)
            db.commit()
            return error_sql.success
        except:
            # db.rollbak()
            return error_sql.error
        db.close()
    else:
        return error_sql.connect_error


# 删除数据
# del_sql为mysql删除语句
def del_data(del_sql):
    if db_connect() != error_sql.connect_error:
        db, cursor = db_connect()
        try:
            cursor.execute(del_sql)
            db.commit()
            return error_sql.success
        except:
            # db.rollbak()
            return error_sql.error
        db.close()
    else:
        return error_sql.connect_error

# if __name__ == '__main__':
#     # text = sql_updata("UPDATE user_admin SET token = '%s' WHERE username = '%s'" % ('sf463ae1gv6ae', 'args'))
#     # print(text)
#     text = get_data("SELECT * FROM iot_device_bind")
