#!/usr/bin/env python
#_*_coding:utf-8_*_
#Python 
#17-7-14    下午6:22
#__author__='Administrator'

import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#print(BASE_DIR)
sys.path.append(BASE_DIR)#加入环境变量

if __name__ == '__main__':
    from modules.actions import excute_from_command_line
    excute_from_command_line(sys.argv)