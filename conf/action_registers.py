#_*_coding:utf-8_*_
import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)#加入环境变量

from modules import views

'''
actions = {
    'start_session': views.start_session,#开始程序
    'stop': views.stop_server,#停止
    'syncdb': views.syncdb,#创建表结构
    'create_users': views.create_users,
    'create_groups': views.create_groups,
    'create_hosts': views.create_hosts,
    'create_bindhosts': views.create_bindhosts,
    'create_remoteusers': views.create_remoteusers,
}
'''
actions = {
    'audit':views.audit,#查看日志
    'start_session': views.start_session,#开始程序
    'stop': views.stop_server,#停止
    'syncdb': views.syncdb,#创建表结构
    'create_users': views.create_users,#创建堡垒机用户
    'create_groups': views.create_groups,#创建分组
    'create_hosts': views.create_hosts,#创建远程主机
    'create_remoteusers': views.create_remoteusers,# #创建远程主机用户
    'create_bindhosts': views.create_bindhosts,# 远程主机与远程主机用户 绑定  关联堡垒机用户与
    #'ass_bind_group': views.ass_bindhost_group,#远程主机与远程主机用户组合 与 分组


}

actionses = {
    'audit                  [查看日志]':views.audit,#查看日志
    'start_session          [开始程序]': views.start_session,#开始程序
    'stop                   [停止]': views.stop_server,#停止
    'syncdb                 [创建表结构]': views.syncdb,#创建表结构
    'create_users           [创建堡垒机用户]': views.create_users,#创建堡垒机用户
    'create_groups          [创建分组]': views.create_groups,#创建分组
    'create_hosts           [创建远程主机]': views.create_hosts,#创建远程主机
    'create_remoteusers     [创建远程主机用户]': views.create_remoteusers,# #创建远程主机用户
    'create_bindhosts       [绑定堡垒机用户与远程主机用户]': views.create_bindhosts,#绑定堡垒机用户与远程主机用户
    #'ass_bind_group         [绑定远程主机+远程主机用户组合与分组]': views.ass_bindhost_group,#远程主机与远程主机用户组合 与 分组


}