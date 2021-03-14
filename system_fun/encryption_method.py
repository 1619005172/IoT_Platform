# -*- coding: utf-8 -*- 
# @Time : 2020/12/29 16:24 
# @Author : kongbai 
# @File : encryption_method.py
# md5加密32位
import hashlib


def md5_pas1(text):
    pw1 = hashlib.md5()
    pw1.update(bytes(text, encoding='utf-8'))
    return pw1.hexdigest()


# sha256加密
def sha256_pas2(text):
    pw2 = hashlib.sha256()
    pw2.update(bytes(text, encoding='utf-8'))
    return pw2.hexdigest()


# 混合后再次进行has256加密
def blend_pw(md5, has256):
    pw3 = md5 + has256
    pw = sha256_pas2(pw3)
    return pw


if __name__ == '__main__':
    text1 = md5_pas1('123123')
    text2 = sha256_pas2('123123')
    print(blend_pw(text1, text2))
