from flask import Flask, request

from api_operation.Android.user_android import testing_key
from api_operation.public_fun import api_get_all, api_get_type, api_get_place, api_get_all_typename, \
    api_get_all_placename, api_get_typename, api_get_placename, api_get_mqtt_allhistory, api_get_mqtt_numhistory, \
    api_get_mqtt_paghistory, user_device_ctrl
from mqtt_operation.mqtt_connect import mqtt_publish, run_mqtt_thread
from system_fun.json_analysis import return_token, return_message, return_data_all
from api_operation.Web_admin.user_admin import login, add_admin, del_admin, get_data_sql, get_type, get_place, \
    add_device_bind, get_online_all, del_device_bind, add_type, add_place, user_add_ctrl_type, user_get_ctrl_type, \
    bind_ctrl_dir
from system_fun.error_code import error_msg, error_re_msg

app = Flask(__name__)
run_mqtt_thread()


# 错误信息返回.提交参数不完整
def err_empty():
    return return_message(error_msg.api_success, error_re_msg.error_empty)


# 错误信息返回.请求api错误
def err_api():
    return return_message(error_msg.api_error, error_re_msg.error)


# 管理员部分
# 用户验证接口
@app.route('/user_admin', methods=['POST', 'GET'])
def user():
    if request.method != 'POST':
        return err_api()
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username, password]):
            return err_empty()
        else:
            data = login(username, password)
            return return_token('200', data[0], data[1])


# 添加用户接口
@app.route('/user_admin/add', methods=['POST'])
def user_add():
    if request.method != 'POST':
        return err_api()
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        mail = request.form.get('mail')
        token = request.form.get('token')
        if not all([username, password, token, mail, phone]):
            return err_empty()
        else:
            data = add_admin(username, password, token, mail, phone)
            return return_message('200', data)


# 删除用户接口
@app.route('/user_admin/del', methods=['POST'])
def user_del():
    if request.method != 'POST':
        return err_api()
    else:
        user_id = request.form.get('user_id')
        token = request.form.get('token')
        if not all([user_id, token]):
            return err_empty()
        else:
            data = del_admin(user_id, token)
            return return_message('200', data)


# 发送报文接口
@app.route('/mqtt_public', methods=['POST'])
def mqtt_public():
    if request.method != 'POST':
        return return_token(400, 'error')
    else:
        mqtt_publish_text = request.form.get('push')
        print('获取接口数据:' + mqtt_publish_text)
        if not all([mqtt_publish_text]):
            return mqtt_publish_text
        else:
            state = mqtt_publish(mqtt_publish_text)
            return return_token('200', state)


# 管理员获取绑定数据
@app.route('/user_admin/get_data', methods=['POST', 'GET'])
def user_get_data():
    if request.method != 'POST':
        return err_api()
    else:
        token = request.form.get('token')
        if not all([token]):
            return err_empty()
        else:
            data = get_data_sql(token)
            # return return_message('200', data)
            print(data)
            return return_data_all(error_msg.api_success, error_re_msg.success, data)


# 管理员获取设备在线数量
@app.route('/user_admin/get_online', methods=['POST', 'GET'])
def user_get_online():
    if request.method != 'POST':
        return err_api()
    else:
        token = request.form.get('token')
        if not all([token]):
            return err_empty()
        else:
            data = get_online_all(token)
            return return_data_all(error_msg.api_success, error_re_msg.success, data)


# 管理员获取设备类型
@app.route('/user_admin/get_device', methods=['POST', 'GET'])
def user_get_device():
    if request.method != 'POST':
        return err_api()
    else:
        token = request.form.get('token')
        if not all([token]):
            return err_empty()
        else:
            return get_type(token)


# 管理员获取设备地址
@app.route('/user_admin/get_place', methods=['POST', 'GET'])
def user_get_place():
    if request.method != 'POST':
        return err_api()
    else:
        token = request.form.get('token')
        if not all([token]):
            return err_empty()
        else:
            return get_place(token)


# 管理员添加设备类型
@app.route('/user_admin/add_type', methods=['POST', 'GET'])
def user_add_type():
    if request.method != 'POST':
        return err_api()
    else:
        token = request.form.get('token')
        type = request.form.get('type')
        name = request.form.get('name')
        if not all([token, type, name]):
            return err_empty()
        else:
            data = add_type(token, type, name)
            return return_message('200', data)


# 管理员添加设备地址
@app.route('/user_admin/add_place', methods=['POST', 'GET'])
def user_add_device():
    if request.method != 'POST':
        return err_api()
    else:
        token = request.form.get('token')
        type = request.form.get('type')
        name = request.form.get('name')
        if not all([token, type, name]):
            return err_empty()
        else:
            data = add_place(token, type, name)
            return return_message('200', data)


# 管理员添加设备
@app.route('/user_admin/add_device_bind', methods=['POST', 'GET'])
def user_add_device_bind():
    if request.method != 'POST':
        return err_api()
    else:
        token = request.form.get('token')
        device_id = request.form.get('device_id')
        place_id = request.form.get('place_id')
        device_name = request.form.get('name')
        device_mac = request.form.get('device_mac')
        if not all([token, device_id, place_id, device_name, device_mac]):
            return err_empty()
        else:
            data = add_device_bind(token, device_id, place_id, device_name, device_mac)
            return return_message(error_msg.api_success, data)


# 管理员删除设备
@app.route('/user_admin/del_device_bind', methods=['POST', 'GET'])
def user_del_device_bind():
    if request.method != 'POST':
        return err_api()
    else:
        token = request.form.get('token')
        device_id = request.form.get('device_id')
        if not all([token, device_id]):
            return err_empty()
        else:
            data = del_device_bind(token, device_id)
            return return_message(error_msg.api_success, data)


# 管理员添加控制类型
@app.route('/user_admin/add_ctrl_type', methods=['POST', 'GET'])
def user_add_ctrl():
    if request.method != 'POST':
        return err_api()
    else:
        token = request.form.get('token')
        type_id = request.form.get('type')
        name = request.form.get('name')
        if not all([token, type_id, name]):
            return err_empty()
        else:
            data = user_add_ctrl_type(token, type_id, name)
            return return_message(error_msg.api_success, data)


# 管理员获取当前控制类型列表
@app.route('/user_admin/get_ctrl_type', methods=['POST', 'GET'])
def user_get_ctrl():
    if request.method != 'POST':
        return err_api()
    else:
        token = request.form.get('token')
        if not all([token]):
            return err_empty()
        else:
            data = user_get_ctrl_type(token)
            return return_message(error_msg.api_success, data)


# 管理员绑定控制指令
@app.route('/user_admin/bind_ctrl_dir', methods=['POST', 'GET'])
def user_bind_ctrl_dir():
    if request.method != 'POST':
        return err_api()
    else:
        token = request.form.get('token')
        type_id = request.form.get('type_id')
        mac = request.form.get('mac')
        name = request.form.get('name')
        data = request.form.get('data')
        if not all([token, type_id, mac, name, data]):
            return err_empty()
        else:
            data = bind_ctrl_dir(token, type_id, mac, name, data)
            return return_message(error_msg.api_success, data)


# 安卓/c#公用部分
# 获取所有设备数据
@app.route('/api/get_data', methods=['POST', 'GET'])
def api_get_data():
    if request.method != 'POST':
        return err_api()
    else:
        key = request.form.get('key')
        # mac = request.form.get('mac')
        if not all([key]):
            return err_empty()
        else:
            data = api_get_all(key)
            print(data)
            # return return_message('200', data)
            # return return_data_all('200', 'success', data)
            return return_data_all(error_msg.api_success, error_re_msg.success, data)


# 获取全部设备类型
@app.route('/api/get_type', methods=['POST', 'GET'])
def api_get_type():
    if request.method != 'POST':
        return err_api()
    else:
        key = request.form.get('key')
        if not all([key]):
            return err_empty()
        else:
            data = api_get_type(key)
            return return_data_all(error_msg.api_success, error_re_msg.success, data)


# 获取设备地址
@app.route('/api/get_place', methods=['POST', 'GET'])
def api_get_pla():
    if request.method != 'POST':
        return err_api()
    else:
        key = request.form.get('key')
        if not all([key]):
            return err_empty()
        else:
            data = api_get_place(key)
            return return_data_all(error_msg.api_success, error_re_msg.success, data)


# 设备所有获取类型名称
@app.route('/api/get_type_all_name', methods=['POST', 'GET'])
def api_get_type_all_name():
    if request.method != 'POST':
        return err_api()
    else:
        key = request.form.get('key')
        if not all([key]):
            return err_empty()
        else:
            data = api_get_all_typename(key)
            return return_data_all(error_msg.api_success, error_re_msg.success, data)


# 获取所有设备地址名称
@app.route('/api/get_place_all_name', methods=['POST', 'GET'])
def api_get_place_all_name():
    if request.method != 'POST':
        return err_api()
    else:
        key = request.form.get('key')
        if not all([key]):
            return err_empty()
        else:
            data = api_get_all_placename(key)
            return return_data_all(error_msg.api_success, error_re_msg.success, data)


# 单个获取设备类型名称
@app.route('/api/get_type_name', methods=['POST', 'GET'])
def api_get_type_name():
    if request.method != 'POST':
        return err_api()
    else:
        key = request.form.get('key')
        type_id = request.form.get('type_id')
        if not all([key, type_id]):
            return err_empty()
        else:
            data = api_get_typename(key, type_id)
            return data


# 单个获取设备地址名称
@app.route('/api/get_place_name', methods=['POST', 'GET'])
def api_get_place_name():
    if request.method != 'POST':
        return err_api()
    else:
        key = request.form.get('key')
        place_id = request.form.get('place_id')
        if not all([key, place_id]):
            return err_empty()
        else:
            data = api_get_placename(key, place_id)
            return data


# 获取指定设备全部历史记录
@app.route('/api/get_mqtt_all_history', methods=['POST', 'GET'])
def api_get_mqtt_all_history():
    if request.method != 'POST':
        return err_api()
    else:
        key = request.form.get('key')
        bind_id = request.form.get('bind_id')
        if not all([key, bind_id]):
            return err_empty()
        else:
            data = api_get_mqtt_allhistory(key, bind_id)
            return return_data_all(error_msg.api_success, error_re_msg.success, data)


# 指定设备历史记录条数查询
@app.route('/api/get_mqtt_num_history', methods=['POST', 'GET'])
def api_get_mqtt_num_history():
    if request.method != 'POST':
        return err_api()
    else:
        key = request.form.get('key')
        bind_id = request.form.get('bind_id')
        if not all([key, bind_id]):
            return err_empty()
        else:
            api_get_mqtt_numhistory(key, bind_id)
            return api_get_mqtt_numhistory(key, bind_id)


# 指定设备历史记录分页查询
@app.route('/api/get_mqtt_pag_history', methods=['POST', 'GET'])
def api_get_mqtt_pag_history():
    if request.method != 'POST':
        return err_api()
    else:
        key = request.form.get('key')
        bind_id = request.form.get('bind_id')
        pag = request.form.get('pag')
        if not all([key, bind_id, pag]):
            return err_empty()
        else:
            print(bind_id, pag)
            data = api_get_mqtt_paghistory(key, bind_id, pag)
            return return_data_all(error_msg.api_success, error_re_msg.success, data)


# # 控制部分(开启、关闭指定设备)
# @app.route('/api/tactics/onoff', methods=['POST', 'GET'])
# def api_tactics_onoff():
#     if request.method != 'POST':
#         return err_api()
#     else:
#         key = request.form.get('key')
#         mac = request.form.get('mac')
#         msg = request.form.get('msg')
#         if not all([key, mac, msg]):
#             return err_empty()
#         else:
#             return

# android单独部分


# 验证key
@app.route('/api/testing_key', methods=['POST', 'GET'])
def android_key():
    if request.method != 'POST':
        return err_api()
    else:
        key = request.form.get('key')
        mac = request.form.get('mac')
        if not all([key, mac]):
            return err_empty()
        else:
            data = testing_key(key, mac)
            print(data)
            return return_message('200', data)


# 设备控制
@app.route('/api/device_ctrl', methods=['POST', 'GET'])
def device_ctrl():
    if request.method != 'POST':
        return err_api()
    else:
        key = request.form.get('key')
        mac = request.form.get('mac')
        instruction_id = request.form.get('instruction_id')
        if not all([key, mac, instruction_id]):
            return err_empty()
        else:
            data = user_device_ctrl(key, mac, instruction_id)
            return return_message(error_msg.api_success, data)


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
