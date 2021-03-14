# -*- coding: utf-8 -*- 
# @Time : 2020/12/22 19:32 
# @Author : kongbai 
# @File : mqtt_connect.py
import threading
import paho.mqtt.client as mqtt
import config_py
from data_sql.mysql_data import get_data, sql_updata, get_data_fix
from data_sql.redis_data import online_state, device_callback_set
from system_fun.error_code import error_sql
from system_fun.generate_tuple import generate_tuple
from system_fun.get_date import get_time
from system_fun.json_analysis import analysis_json


# 连接服务器回调
def on_connect(client, userdata, flags, rc):
    print("与服务器连接" + str(rc))
    # 订阅主题
    client.subscribe(config_py.mqtt_topic)
    client.subscribe('$SYS/brokers/+/clients/+/connected')
    client.subscribe('$SYS/brokers/+/clients/+/disconnected')
    client.subscribe(config_py.mqtt_response_topic)


# 收到消息回调
def on_message(client, userdata, msg):
    print("mqtt客户端接收数据:" + msg.topic + ":" + str(msg.payload) + str(get_time()))
    # 设备上线处理
    if '$SYS' in msg.topic:
        system_msg(msg)
    elif config_py.mqtt_response_topic in msg.topic:
        mqtt_response(msg, config_py.mqtt_response_topic)
        print('控制消息')
    else:
        topic_msg(msg, config_py.mqtt_topic)
        print('普通消息')

    # config_py.mqtt_msg = str(msg.payload)


# 获取数据库设备绑定记录
def get_bind(device_mac):
    data = get_data("SELECT * FROM iot_device_bind WHERE mac = '%s'" % device_mac)
    if data:
        return True
    else:
        return False


# 设备上下线记录
def up_online(num, device_mac):
    args = (num, device_mac)
    print(args)
    data = sql_updata("UPDATE iot_device_bind SET online = '%s' WHERE mac = '%s'" % args)
    return data


# 消息处理自增线程
def connected(msg):
    print('设备上线成功')
    data = analysis_json(msg.payload)
    if get_bind(data["clientid"]):
        up_online(1, data['clientid'])
        # online_state(data['clientid'], 1)
    else:
        print('此设备未绑定')


def disconnected(msg):
    data = analysis_json(msg.payload)
    print("设备" + data['clientid'] + "下线")
    if get_bind(data["clientid"]):
        up_online(0, data['clientid'])
        # online_state(data['clientid'], 0)
    else:
        print('此设备未绑定')


# # 消息处理线程启动
# def run_msg_treading():
#

# 系统主题消息处理
def system_msg(msg):
    if 'server_py' in msg.topic:
        return 0
    else:
        try:
            if 'disconnected' in msg.topic:
                data = analysis_json(msg.payload)
                print("设备" + data['clientid'] + "下线")
                if get_bind(data["clientid"]):
                    up_online(0, data['clientid'])
                    # online_state(data['clientid'], 0)
                else:
                    print('此设备未绑定')
            elif 'connected' in msg.topic:
                print('设备上线成功')
                data = analysis_json(msg.payload)
                if get_bind(data["clientid"]):
                    up_online(1, data['clientid'])
                    # online_state(data['clientid'], 1)
                else:
                    print('此设备未绑定')
        except:
            print('消息处理异常')


# 普通订阅主题消息处理
def topic_msg(msg, topic):
    if msg.topic == topic:
        try:
            data = analysis_json(msg.payload)
            mac = data['mac']
            msg = data['data'].items()
            msg2 = ''
            for key, values in msg:
                msg2 = msg2 + key + ':' + values + '|'
            print(msg2)
            # 验证mac是否存在
            if get_bind(mac):
                # if data['getway']:
                #     # 网关消息处理
                #     getway = data['getway']
                #     if get_bind(getway):
                #         print('网关操作')
                # else:
                # 普通设备消息处理
                data1, data_list = get_data_fix("SELECT * FROM iot_device_bind WHERE mac = '%s'" % mac)
                data = generate_tuple(data_list, data1, 'bind')[0]
                args = (data['place_id'], get_time(), data['id'], msg2)
                args2 = (data['place_id'], str(get_time()), data['id'], msg2)
                print(args)
                # 存储消息历史
                sql_msg = sql_updata("INSERT INTO iot_mqtt_historical (place_id,date ,bind_id,data) "
                                     "VALUES ('%s','%s','%s','%s')" % args)
                if sql_msg == error_sql.success:
                    print("写入记录成功")
                else:
                    print("写入记录失败")
            else:
                print('此设备未绑定')
        except:
            print('消息处理出错')
    else:
        print('系统主题消息')


# 设备消息返回主题处理
def mqtt_response(msg, topic):
    if msg.topic == topic:
        try:
            data = analysis_json(msg.payload)
            mac = data['mac']
            msg = data['data']
            print(msg)
            config_py.mqtt_msg = msg
            device_callback_set(mac, msg)
        except:
            print('消息格式错误')


# mqtt消息发布
def mqtt_publish(mqtt_publish_text):
    try:
        state = client.publish(config_py.mqtt_send_topic, payload=mqtt_publish_text, qos=0, retain=False)
        print('发送报文:' + mqtt_publish_text)
        if state.rc == mqtt.MQTT_ERR_SUCCESS:
            return "PUBLISH_SUCCESS"
        else:
            return "ERROR"
    except:
        return 'MQTT_ERROR'


try:
    client = mqtt.Client(client_id=config_py.mqtt_clientID)
    client.username_pw_set(config_py.mqtt_username, config_py.mqtt_passwd)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(config_py.mqtt_host, config_py.mqtt_port, config_py.mqtt_time)
except:
    print('mqtt连接失败')


# mqtt线程
class mqtt_threading(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self) -> None:
        # 阻塞式连接
        client.loop_forever()


def run_mqtt_thread():
    thread_mqtt1 = mqtt_threading(1, "mqtt_thread", 1)
    thread_mqtt1.start()
