#_*_coding:utf-8_*_

import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USER='root'#用户名
PASSWORD='root'#密码
HOST_IP='127.0.0.1'#数据库地址
PORT="3306"#数据库端口
DB='little_finger'#库名
DB_CONN ="mysql+pymysql://"+USER+":"+PASSWORD+"@"+HOST_IP+":"+PORT+"/"+DB+"?charset=utf8"#连接参数
#DB_CONN ="mysql+pymysql://root:root@localhost:3306/"+DB+"?charset=utf8"#连接参数

'''
# Database
DATABASES = {
    'default': {
        'ENGINE': 'mysqldb',
        'NAME': 'LittleFinger',
        'HOST': '',
        'PORT':3306,
        'USER':'root',
        'PASSWORD': ''
    }
}
'''

