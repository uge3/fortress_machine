#_*_coding:utf-8_*_
__author__ = 'Alex Li'


from conf import settings
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def print_err(msg,quit=False):#错误提示输出
    output = "\033[31;1mError: %s\033[0m" % msg
    if quit:
        exit(output)
    else:
        print(output)


def yaml_parser(yml_filename):
    '''
    load yaml file and return
    :param yml_filename:
    :return:
    '''
    #yml_filename = "%s/%s.yml" % (settings.StateFileBaseDir,yml_filename)
    try:
        yaml_file = open(yml_filename,'r')#打开文件
        data = yaml.load(yaml_file)#load 成一个对象
        return data#返回数据
    except Exception as e:
        print_err(e)
