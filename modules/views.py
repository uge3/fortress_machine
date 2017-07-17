#_*_coding:utf-8_*_
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)#加入环境变量
from modules import models
from modules.db_conn import engine,session
from modules.utils import print_err,yaml_parser
#from modules import common_filt
from modules import ssh_login
from sqlalchemy import create_engine,Table
from  sqlalchemy.orm import sessionmaker

from conf import settings

#用户登陆函数
def auth():
    '''
    do the user login authentication
    :return:
    '''
    count = 0
    while count <3:#用户输入三次机会
        username = input("\033[32;1mUsername:\033[0m").strip()
        if len(username) ==0:continue
        password = input("\033[32;1mPassword:\033[0m").strip()
        if len(password) ==0:continue
        user_obj = session.query(models.UserProfile).filter(models.UserProfile.username==username,
                                                            models.UserProfile.password==password).first()#从数据库中获取堡垒机用户信息
        if user_obj:
            return user_obj
        else:
            print("wrong username or password, you have %s more chances." %(3-count-1))
            count +=1
    else:
        print_err("too many attempts.")


#欢迎界面
def welcome_msg(user):
    WELCOME_MSG = '''\033[32;1m
    ------------- Welcome [%s] login LittleFinger -------------
    \033[0m'''%  user.username
    print(WELCOME_MSG)


#写入数据库 日志
def log_recording(user_obj,bind_host_obj,logs):
    '''
    flush user operations on remote host into DB
    :param user_obj:
    :param bind_host_obj:
    :param logs: list format [logItem1,logItem2,...]
    :return:
    '''
    print("\033[41;1m--logs:\033[0m",logs)
    session.add_all(logs)
    session.commit()

#开始函数
def start_session(argvs):
    print('going to start sesssion ')
    user = auth()#判断用户名 并返回用户对应信息
    if user:
        welcome_msg(user)#打印欢迎界面
        #print(user.id)#用户ID
        #print(user.bind_hosts)#绑定主机
        #print(user.host_group)#所在组
        #log_recording(user,user.bind_hosts,user.host_group,logs)
        exit_flag = False#设定点 为假
        while not exit_flag:#如果设定点 为假 说明登陆成功
            if user.bind_hosts:#有绑定远程主机 打印远程主机
                print('\033[32;1mz.\tungroupped hosts (%s)\033[0m' %len(user.bind_hosts) )
            for index,group in enumerate(user.host_group):#打印当前用户所在组
                print('\033[32;1m%s.\t%s (%s)\033[0m' %(index,group.group_name,  len(group.bind_host)) )

            print('(q)=quit')
            choice = input("[%s]:" % user.username).strip()#开始获取输入的命令

            if len(choice) == 0:continue#如果没有输入跳过
            if choice == 'q':
                exit_flag=True
            #if choice=='exit': exit()#退出
            if choice == 'z':#如果输入 z
                print("------ Group: ungroupped hosts ------" )#输出所有的未分组的主机
                for index,bind_host in enumerate(user.bind_hosts):
                    print("  %s.\t%s@%s(%s)"%(index,
                                              bind_host.remote_user.username,#绑定的用户名
                                              bind_host.host.hostname,#主机名
                                              bind_host.host.ip,#IP地址
                                              ))
                print("----------- END -----------" )
            elif choice.isdigit():#如果是选择数字
                choice = int(choice)
                if choice < len(user.host_group):
                    print("------ Group: %s ------"  % user.host_group[choice].group_name )
                    for index,bind_host in enumerate(user.host_group[choice].bind_host):#打印出选择组的包括的
                        print("  %s.\t%s@%s(%s)"%(index,
                                                  bind_host.remote_user.username,#绑定的用户名
                                                  bind_host.host.hostname,#主机名
                                                  bind_host.host.ip,#IP地址
                                                  ))
                    print("----------- END -----------" )

                    #host selection
                    while not exit_flag:
                        user_option = input("[(b)back, (q)quit, select host to login]:").strip()
                        if len(user_option)==0:continue
                        if user_option == 'b':break
                        if user_option == 'q':
                            exit_flag=True
                        if user_option.isdigit():
                            user_option = int(user_option)
                            if user_option < len(user.host_group[choice].bind_host) :#查看分组所绑定的远程 主机
                                print('host:',user.host_group[choice].bind_host[user_option])
                                print('audit log:',user.host_group[choice].bind_host[user_option].audit_logs)
                                ssh_login.ssh_login(user,
                                                    user.host_group[choice].bind_host[user_option],
                                                    session,
                                                    log_recording)
                else:
                    print("no this option..")

#停止退出
def stop_server(argvs):
    exit()

#创建表结构
def syncdb(argvs):
    print("Syncing DB....[创建所有表结构]")
    models.Base.metadata.create_all(engine) #创建所有表结构

'''======创建四个基础表====  '''
#堡垒机用户添加
def create_users(argvs):
    if '-f' in argvs:#判断参数 -f 是否存在
        user_file  = argvs[argvs.index("-f") +1 ]#获取文件位置
    else:
        print_err("invalid usage, should be:\ncreateusers -f <the new users file>",quit=True)
    source = yaml_parser(user_file)#获取文件内容数据
    if source:#如果获取成功
        for key,val in source.items():
            print(key,val)
            obj = models.UserProfile(username=key,password=val.get('password'))#创建新数据
            session.add(obj)
        session.commit()

#分组添加
def create_groups(argvs):
    if '-f' in argvs:#判断参数 -f 是否存在
        group_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("invalid usage, should be:\ncreategroups -f <the new groups file>",quit=True)
    source = yaml_parser(group_file)#通过yaml 获取文件中的数据,
    if source:
        for key,val in source.items():
            print(key,val)
            obj = models.HostGroup(group_name=key)#创建一条新数据
            if val.get('bind_hosts'):#
                bind_hosts = bind_hosts_filter(val)#绑定的远程主机组合表
                obj.bind_host = bind_hosts
            if val.get('user_profiles'):#堡垒机用户
                user_profiles = user_profiles_filter(val)#堡垒机用户
                obj.user_profiles = user_profiles
            session.add(obj)
        session.commit()

#远程主机添加
def create_hosts(argvs):
    if '-f' in argvs:#判断参数 -f 是否存在
        hosts_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("invalid usage, should be:\ncreate_hosts -f <the new hosts file>",quit=True)#退出函数
    source = yaml_parser(hosts_file)#通过yaml 获取文件中的数据,
    if source:#如果获取成功,不为空
        for key,val in source.items():#进行数据的解析
            print(key)
            print(val)
            obj = models.Host(hostname=key,ip=val.get('ip'), port=val.get('port') or 22)#port 端口默认为22
            session.add(obj)#写入到数据库
        session.commit()#关闭 确认写入

#创建远程主机用户
def create_remoteusers(argvs):
    if '-f' in argvs:
        remoteusers_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("invalid usage, should be:\ncreate_remoteusers -f <the new remoteusers file>",quit=True)
    source = yaml_parser(remoteusers_file)#通过yaml 获取文件中的数据,
    if source:
        for key,val in source.items():#进行数据的解析
            print(key,val)
            obj = models.RemoteUser(username=val.get('username'),auth_type=val.get('auth_type'),password=val.get('password'))
            session.add(obj)#写入数据库
        session.commit()


'''====远程主机与远程主机用户组合表====='''
##远程主机用户名密码与远程主机组合绑定   关联 到堡垒机用户
def create_bindhosts(argvs):
    if '-f' in argvs:
        bindhosts_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("invalid usage, should be:\ncreate_hosts -f <the new bindhosts file>",quit=True)
    source = yaml_parser(bindhosts_file)#通过yaml 获取文件中的数据,
    if source:
        for key,val in source.items():
            print(key,val)
            host_obj = session.query(models.Host).filter(models.Host.hostname==val.get('hostname')).first()#获取对应主机数据
            assert host_obj#断言 当前主机一定要存在才能往下执行
            for item in val['remote_users']:#输出存在的远程主机用户
                print(item )
                assert item.get('auth_type')#断言 一定要存在才能往下执行
                if item.get('auth_type') == 'ssh-passwd':#判断ssh连接类型 从数据库选出合条件的数据
                    remoteuser_obj = session.query(models.RemoteUser).filter(
                                                        models.RemoteUser.username==item.get('username'),
                                                        models.RemoteUser.password==item.get('password')
                                                    ).first()#获取主机数据 返回对象
                else:
                    remoteuser_obj = session.query(models.RemoteUser).filter(
                                                        models.RemoteUser.username==item.get('username'),
                                                        models.RemoteUser.auth_type==item.get('auth_type'),
                                                    ).first()
                if not remoteuser_obj:#如果远程主机用户不存在
                    print_err("RemoteUser obj %s does not exist." % item,quit=True )
                bindhost_obj = models.BindHost(host_id=host_obj.id,remote_user_id=remoteuser_obj.id)#创建一条新数据
                session.add(bindhost_obj)
                #for groups this host binds to
                if source[key].get('groups'):#如果有分组标志
                    #获取分组信息
                    group_objs = session.query(models.HostGroup).filter(models.HostGroup.group_name.in_(source[key].get('groups') )).all()
                    assert group_objs#断言  分组一定要存在才能往下执行
                    print('groups:', group_objs)
                    bindhost_obj.host_groups = group_objs#主机加到分组
                #for user_profiles this host binds to
                if source[key].get('user_profiles'):#如果有堡垒机用户标志
                    #获取堡垒机用信息
                    userprofile_objs = session.query(models.UserProfile).filter(models.UserProfile.username.in_(
                        source[key].get('user_profiles')
                    )).all()
                    assert userprofile_objs#断言 堡垒机用户一定要存在才能往下执行
                    print("userprofiles:",userprofile_objs)
                    bindhost_obj.user_profiles = userprofile_objs#主机与堡垒机用户绑定
                #print(bindhost_obj)
        session.commit()


#远程主机组合表查看
def bind_hosts_filter(vals):#远程主机组合表查看
    print('**>',vals.get('bind_hosts') )
    bind_hosts = session.query(models.BindHost).filter(models.Host.hostname.in_(vals.get('bind_hosts'))).all()
    if not bind_hosts:
        print_err("none of [%s] exist in bind_host table." % vals.get('bind_hosts'),quit=True)
    return bind_hosts

#堡垒机用户查看
def user_profiles_filter(vals):
    user_profiles = session.query(models.UserProfile).filter(models.UserProfile.username.in_(vals.get('user_profiles'))).all()
    if not user_profiles:
        print_err("none of [%s] exist in user_profile table." % vals.get('user_profiles'),quit=True)
    return  user_profiles



#查看用户日志
def audit(argvs):
    if '-n' in argvs:
        user_name  = argvs[argvs.index("-n") +1 ]#获取要查看的用户名
    else:
        print_err("invalid usage, should be:\n输入参数 -n <用户名/user_name >",quit=True)
    print(user_name)
    user_obj = session.query(models.UserProfile).filter(models.UserProfile.username==user_name).first()#取到
    print(user_obj.id)
    log_obj = session.query(models.AuditLog).filter(models.AuditLog.user_id==user_obj.id).all()
    for i in log_obj:
        print('堡垒机用户：【%s】,远程主机【%s】,远程用户：【%s】命令：【%s】,日期：【%s】'%(i.user_profile,i.bind_host.host,i.bind_host.remote_user,i.cmd,i.date))
    input('========')


