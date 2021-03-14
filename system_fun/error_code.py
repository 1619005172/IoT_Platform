# -*- coding: utf-8 -*- 
# @Time : 2021/1/7 11:29 
# @Author : kongbai 
# @File : error_code.py


# 全局错误信息.api错误代码
class error_msg:
    api_error = 404
    api_success = 200


# 全局错误信息.数据库错误
class error_sql:
    connect_error = 'connect_error'
    error = 'error'
    success = 'success'


# 全局错误信息.api返回错误
class error_re_msg:
    error = 'error'
    success = 'success'
    error_empty = 'error_empty'


# 全局错误信息.用户错误
class err_user:
    empty = 'None'
    error = 'error'
    success = 'success'
    no_user = 'no_user'
    user_already = 'username_already'
    authority = 'Permission_denied'
    key_success = 'key_success'
    key_error = 'key_error'
    key_activation = 'key_activation'
