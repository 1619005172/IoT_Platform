# -*- coding: utf-8 -*-
# @Time : 2021/1/22 15:26 
# @Author : kongbai 
# @File : send_mail.py
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from data_sql.mysql_data import get_data_fix
from system_fun.generate_tuple import generate_tuple


def get_config():
    try:
        data, data_list = get_data_fix(
            "SELECT sendmail,pass,mailserver,mailport,subject,servername FROM iot_server_config")
        # data, data_list = get_data("SELECT * FROM iot_server_config")
        data1 = generate_tuple(data_list, data, 'bind')
        # print(data1[0])
        # data1 = data[0][0], data[0][1], data[0][2], data[0][3], data[0][4]
        # print(data1)
        config = data1[0]
        print(config.get('sendmail'))
        return config
    except:
        return 'sql_error'


# 批量发送邮件
def send_mail(acc_num, message):
    conf = get_config()
    try:
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = formataddr([conf.get('servername'), conf.get('sendmail')])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        # msg['To'] = formataddr(["Kongbai", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = conf.get('subject')  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL(conf.get('mailserver'), conf.get('mailport'), 'utf-8')  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(conf.get('sendmail'), conf.get('pass'))  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(conf.get('sendmail'), acc_num, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print('发送成功')
        return 'success'
    except Exception:
        print('发送失败')
        return 'error'


# if __name__ == '__main__':
#     num = ['1619005172@qq.com', '64074652@qq.com']
#     send_mail(num, '测试信息')
    # get_config()
