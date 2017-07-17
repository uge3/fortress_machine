堡垒机
windows ,linux 都通过测试
初始化说明：
    #进入根目录
    1、初始化表结构   #python3 bin/start.py syncdb
    2、创建堡垒机用户 #python3 bin/start.py create_users -f share/examples/new_user.yml
    3、创建分组       #python3 bin/start.py create_groups -f share/examples/new_groups.yml
    4、创建远程主机   #python3 bin/start.py create_hosts -f share/examples/new_hosts.yml
    5、创建远程主机用户（绑定堡垒机用户与分组）#python3 bin/start.py create_remoteusers -f share/examples/new_remoteusers.yml
    6、绑定远程主机与远程主机用户【远程绑定组合】（关联远程绑定组合与堡垒机用户、关联远程绑定组合与分组）
        #python3 bin/start.py create_bindhosts -f share/examples/new_bindhosts.yml
    7、登陆堡垒机    #python3 bin/start.py start_session  （示例用户： uge3 密码：uge3）
    8、查看用户日志      #python3 bin/start.py audit -n uge3


plj/#程序目录
|- - -__init__.py
|- - -bin/#启动目录
|      |- - -__init__.py
|      |- - -start.py#启动
|
|- - -conf/#配置目录
|      |- - -__init__.py
|      |- - -action_registers.py#开始参数配置文件
|      |- - -settings.py#配置文件
|
|- - -modules/#主逻辑目录
|      |- - -__init__.py
|      |- - -actions.py#开始函数 帮助信息
|      |- - -db_conn.py#数据库连接配置
|      |- - -interactive.py#ssh命令重写
|      |- - -models.py#表结构 类
|      |- - -ssh_login.py#登陆远程主机调用
|      |- - -utils.py#工具函数
|      |- - -views.py#主要逻辑函数
|
|- - -REDMAE
|
|- - -share/#添加堡垒机用户\远程主机\分组\远程主机用户 目录
|      |- - -examples/#文件目录
|              |- - -new_bindhosts.yml/#远程主机用户与远程主机 组合表（组合表与 分组）（堡垒机用户与组合表） 创建 示例
|              |- - -new_groups.yml/#分组创建 示例（ 堡垒机用户与 分组）
|              |- - -new_hosts.yml/#远程主机创建 示例
|              |- - -new_remoteusers.yml/#远程主机用户创建 示例
|              |- - -new_user.yml/#堡垒机用户机创建 示例
|
