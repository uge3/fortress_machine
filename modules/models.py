#!/usr/bin/env python
#_*_coding:utf-8_*_
#Python 
#17-7-12    上午10:54
#__author__='Administrator'

# 创建表
import os ,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#获取相对路径转为绝对路径赋于变量
sys.path.append(BASE_DIR)#增加环境变量
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index,Table,DATE,DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy import func #统计
from sqlalchemy_utils import ChoiceType,PasswordType #
from  conf import settings
Base = declarative_base()#生成orm 基类

# #创建堡垒机用户关联－－联合表,自动维护
user_profile_m2m_bind_host = Table('user_profile_m2m_bind_host', Base.metadata,
                        Column('user_profile_id',Integer,ForeignKey('user_profile.id')),#关联,用户id
                        Column('bind_host_id',Integer,ForeignKey('bind_host.id')),#关联,联合表id
                        )
# #创建联合表－－分组,自动维护
bind_host_m2m_host_group = Table('bind_host_m2m_host_group', Base.metadata,
                        Column('bind_host_id',Integer,ForeignKey('bind_host.id')),#关联,联合表id
                        Column('host_group_id',Integer,ForeignKey('host_group.id')),#关联,分组id
                        )
# #创建堡垒机用户－－分组,自动维护
user_profile_m2m_host_group = Table('user_profile_m2m_host_group', Base.metadata,
                        Column('user_profile_id',Integer,ForeignKey('user_profile.id')),#关联,堡垒机用户id
                        Column('host_group_id',Integer,ForeignKey('host_group.id')),#关联,分组id
                        )
#主机表
class Host(Base):#主机表
    __tablename__='host'
    id=Column(Integer,primary_key=True)
    hostname=Column(String(64),unique=True)#主机名
    ip=Column(String(64),unique=True)#ip
    port=Column(Integer,default=22)#端口默认为22
    def __repr__(self):
        return self.hostname#输出主机名

#服务器远程主机用户名密码
class RemoteUser(Base):
    __tablename__='remote_user'

    id=Column(Integer,primary_key=True)
    AuthType=[
        ('ssh-passwd','SSH-Password'),
        ('ssh-key','SSH-Key'),
    ]
    auth_type=Column(ChoiceType(AuthType))#认证类型
    username=Column(String(64))#用户名 不用唯一
    password=Column(String(64))
    __table_args__=(UniqueConstraint('auth_type','username','password',name='user_password_type'),)#联合只唯一
    def __repr__(self):
        return self.username#用户名

#绑定远程主机-远程用户关联表
class BindHost(Base):
    __tablename__='bind_host'
    __table_args__=(UniqueConstraint('host_id',"remote_user_id",name='host_id_remote'),)#联合唯一
    id=Column(Integer,primary_key=True)
    host_id=Column(Integer,ForeignKey('host.id'))#外键－－〉主机表
    remote_user_id=Column(Integer,ForeignKey('remote_user.id'))#外键－－〉主机用户表
    host=relationship('Host',backref='bind_hosts')#外键  主机表 查询与反查
    remote_user=relationship('RemoteUser',backref='bind_hosts')#外键 用户表 查询与反查
    def __repr__(self):
        return '[主机：%s----->登陆用户：%s]'%(self.host.ip,self.remote_user.username)#


#主机分组
class HostGroup(Base):
    __tablename__='host_group'
    id=Column(Integer,primary_key=True)
    group_name=Column(String(64),unique=True)#主机分组名
    bind_host=relationship('BindHost',secondary=bind_host_m2m_host_group,backref='host_groups')#分组表 远程联合表 查询与反查
    def __repr__(self):
        return self.group_name#输出主机名

#堡垒机用户,
class UserProfile(Base):
    __tablename__='user_profile'
    id=Column(Integer,primary_key=True)
    username=Column(String(64),unique=True)#用户名
    password=Column(String(256))
    bind_hosts = relationship('BindHost',secondary=user_profile_m2m_bind_host,backref='user_profiles')#调用关联绑定表查看 堡垒机用户名
    host_group = relationship('HostGroup',secondary=user_profile_m2m_host_group,backref='user_profiles')#调用关联 分组查看 堡垒机用户名
    #audit_logs = relationship('AuditLog')#查日志
    def __repr__(self):
        return self.username#用户名

#日志类
class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('user_profile.id'))#外键  堡垒机用户ID
    bind_host_id = Column(Integer,ForeignKey('bind_host.id'))#外键  远程主机ID
    action_choices = [
        (u'cmd',u'CMD'),#命令
        (u'login',u'Login'),#登陆
        (u'logout',u'Logout'),#退出
    ]
    action_type = Column(ChoiceType(action_choices))#日志类型
    cmd = Column(String(255))#命令
    date = Column(DateTime)#日期时间
    user_profile = relationship("UserProfile",backref='audit_logs')#关联堡垒机用户  查询
    bind_host = relationship("BindHost",backref='audit_logs')#关联远程主机   查询