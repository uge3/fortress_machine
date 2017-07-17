#!/usr/bin/env python
#_*_coding:utf-8_*_
#Python 
#17-7-14    下午6:25
#__author__='Administrator'
import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)#加入环境变量

from conf import settings
from conf import action_registers
from modules import utils


def help_msg():#帮助信息
    '''
    print help msgs
    :return:
    '''
    print("\033[31;1mAvailable commands:\033[0m")
    for key in action_registers.actionses:#打印配置文件中的帮助信息
        print("\t",key)


def excute_from_command_line(argvs):#接收输入的命令
    if len(argvs) < 2: #如果小于两个词
        help_msg()#打印帮助信息
        exit()
    if argvs[1] not in action_registers.actions:
        utils.print_err("Command [%s] does not exist!" % argvs[1], quit=True)
    action_registers.actions[argvs[1]](argvs[1:])#获取到命令