# -*- coding:utf-8 _*-  
__author__ = 'luyue'
""" 
@file: email_send.py 
@time: 2018/03/{DAY} 
"""

from users.models import EmailVerifyRecord
from random import Random
from MookOnline.settings import EMAIL_FROM

from django.core.mail import send_mail


def random_str(randomlength = 8):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    email_str = ''
    random = Random()

    for i in range(randomlength):
        email_str += chars[random.randint(0, len(chars)-1)]
    return email_str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    email_record.email = email
    code = random_str(16)
    email_record.code = code
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if email_record.send_type == 'register':
        email_title = '欢迎注册墓穴在线'
        email_body = '请点击链接以完成注册:http://127.0.0.1:8000/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print("发送成功")
            return True
        else:
            return False

    elif email_record.send_type == 'forget':
        email_title = '欢迎重置墓穴在线'
        email_body = '请点击链接以完成重置密码:http://127.0.0.1:8000/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print("发送成功")
            return True
        else:
            return False

    elif email_record.send_type == 'update_email':
        email_title = '欢迎墓穴在线'
        email_body = '邮箱验证码为：{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print("发送成功")
            return True
        else:
            return False
