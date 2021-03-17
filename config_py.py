# -*- coding: utf-8 -*- 
# @Time : 2020/12/23 9:32 
# @Author : kongbai 
# @File : config_py.py
mqtt_msg = None
publish_i = None

# mqtt服务器地址
mqtt_host = "10.67.42.72"
# mqtt服务器端口
mqtt_port = 1883
# mqtt心跳时间
mqtt_time = 60
# mqtt连接id
mqtt_clientID = 'server_test'
# mqtt连接用户名
mqtt_username = 'server_test'
# mqtt连接密码
mqtt_passwd = '123456'
# 接收消息主题
mqtt_topic = 'test'
# 发送消息主题
mqtt_send_topic = 'send_test'
# 设备响应消息主题
mqtt_response_topic = 'response_test'
# 客户端订阅主题
mqtt_client_topic = 'app_client_topic'

# 数据库地址
db_url = '127.0.0.1'
# 数据库用户名
db_user = 'root'
# 数据库密码
db_passwd = 'root'
# 数据库名
db_from = 'flask_mqtt'

# redis地址
r_host = 'localhost'
# redis端口
r_port = 6379
# redis密码
r_passwd = '666666'
