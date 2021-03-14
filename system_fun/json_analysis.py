# -*- coding: utf-8 -*- 
# @Time : 2020/12/24 12:42 
# @Author : kongbai 
# @File : json_analysis.py
# json解析以及构建
import json


def return_token(code, message, token):
    data = json.dumps({'code': code, 'message': message, 'data': {'token': token}},
                      sort_keys=True, indent=4, separators=(',', ':'))
    return data


def return_message(code, message):
    data = json.dumps({'code': code, 'message': message}, ensure_ascii=False, sort_keys=True, indent=4,
                      separators=(',', ':'))
    return data


# json解析,将json字符串转换为字典
def analysis_json(json_str):
    data = json.loads(json_str)
    return data


def return_data_all(code, message, data):
    data_json = json.dumps({'code': code, 'message': message, 'data': data},
                           ensure_ascii=False, indent=4, separators=(',', ':'))
    return data_json


# 生成json
def generate_json(data):
    data_json = json.dumps(data, ensure_ascii=False, indent=4, separators=(',', ':'))
    return data_json
