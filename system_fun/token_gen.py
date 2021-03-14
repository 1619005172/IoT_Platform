# -*- coding: utf-8 -*- 
# @Time : 2020/12/28 15:09 
# @Author : kongbai 
# @File : token_gen.py
# 生成token
import random
import string
import time

from system_fun.encryption_method import md5_pas1, sha256_pas2


# 获取当前时间
def get_time():
    try:
        date = time.asctime()
        # print(date)
        return date
    except:
        # print("时间获取失败")
        return "error"


# 从a-zA-Z0-9生成指定数量的随机字符：
def get_random():
    text = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    # print(text)
    return text


# 生成token
def token_gen():
    text = get_time() + get_random()
    token = md5_pas1(sha256_pas2(text))
    print(token)
    return token
