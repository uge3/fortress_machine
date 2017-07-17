#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#python 
#2017/7/15    19:44
#__author__='Administrator'


import base64
import getpass
import os
import socket
import sys
import traceback
from paramiko.py3compat import input
from  modules import models
import datetime

import paramiko
try:
    import interactive
except ImportError:
    from . import interactive

#登陆远程主机
def ssh_login(user_obj,bind_host_obj,mysql_engine,log_recording):#ssh进入远程主机
    # now, connect and use paramiko Client to negotiate SSH2 across the connection
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        print('*** Connecting...')#开始连接
        #client.connect(hostname, port, username, password)
        client.connect(bind_host_obj.host.ip,
                       bind_host_obj.host.port,
                       bind_host_obj.remote_user.username,
                       bind_host_obj.remote_user.password,
                       timeout=30)#超时30秒

        cmd_caches = []#定义一个列表,暂时保存命令
        chan = client.invoke_shell()
        print(repr(client.get_transport()))
        print('*** Here we go!\n')
        cmd_caches.append(models.AuditLog(user_id=user_obj.id,
                                          bind_host_id=bind_host_obj.id,
                                          action_type='login',
                                          date=datetime.datetime.now()
                                          ))
        log_recording(user_obj,bind_host_obj,cmd_caches)
        interactive.interactive_shell(chan,user_obj,bind_host_obj,cmd_caches,log_recording)#传入 堡垒机用户, 连接远程主机 命令 记当日志函数
        chan.close()
        client.close()

    except Exception as e:
        print('*** Caught exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
        try:
            client.close()
        except:
            pass
        sys.exit(1)