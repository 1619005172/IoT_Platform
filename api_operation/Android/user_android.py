# -*- coding: utf-8 -*- 
# @Time : 2021/1/6 10:00 
# @Author : kongbai 
# @File : user_android.py
from data_sql.mysql_data import get_data_fix, sql_updata, get_data
from system_fun.error_code import err_user


# 验证key
def testing_key(key, mac):
    args = (key, mac)
    data_key, key_list = get_data_fix("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'" % args[0])
    if data_key:
        data = get_data("SELECT * FROM iot_cdk_cdk WHERE cdk = '%s'AND mac = '%s'" % args)
        print(data)
        if data:
            print('验证成功')
            return err_user.key_success
        else:
            sql_updata("UPDATE iot_cdk_cdk SET mac = '%s' WHERE cdk = '%s'" % (args[1], args[0]))
            return err_user.key_activation
    else:
        print('无效key')
        return err_user.key_error

# if __name__ == '__main__':
#     testing_key('6938EC5F52BECAE00F583E4F02D056D8', '1341')
