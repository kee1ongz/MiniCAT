#    miniapp_dict = gl.get_value("miniapp_dict")
#    query_dir = gl.get_value("query_dir")
#    #ide_cli = gl.get_value("ide_cli")
#    dirs = os.listdir(miniapp_dict)
#    if dirs is None:
#        print("Nothing in your miniapp_dict,Please check your config file.")
#        exit(1)
#    print(dirs)
#    if not os.path.exists(query_dir+"/dec_dir"):
#        print("[*]Crating dec_dir:save decrypted applets.")
#        os.mkdir(query_dir+"/dec_dir")
#    #gl.set_value("dec_dir",query_dir+"/dec_dir")
#    dec_dir = gl.get_value("dec_dir")
#    gl.set_value("res_dir",query_dir+"/res")
#    #appid_list = []
#    not_empty = False
#    for sub_dir in dirs:

# -*- coding:utf-8 -*-
import argparse
import configparser
import utility.globalvar as gl
import codeql_query.MiniCSRF_detect
from codeql_query import *
import threading
import logging
import datetime
import sys
import subprocess
import shutil
import time
import traceback
import os

# 修改ArgumentParser部分
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--appid', help='The appid of your mini-program.')  # 修改-s参数的说明
parser.add_argument('-p', '--platform', choices=['wechat', 'baidu'], default='wechat', help='The platform you want to analyze.')  # 添加-p参数
parser.add_argument('-sp', '--source', choices=['windows', 'android'], default='windows', help='Choose the source platform of your mini-app.')
parser.add_argument('-dec', '--justdecrypted', choices=['yes', 'no'], default='no', help='Just Using MiniCAT for decrypting Mini-programs')
# Read the INI config file in the root directory.
def read_ini():
    gl._init()
    print("[*]Reading configuration from config.ini...")
    try:
        config = configparser.ConfigParser()
        config.read("./config.ini", encoding='utf-8')
        # read miniapp_dict and query_dir
        miniapp_dict = config.get('Query Paths', 'miniapp_dict')
        query_dir = config.get('Query Paths', 'query_dir')
        dec_dir = config.get('Query Paths','dec_dir')
        # (windows only) read Wechat IDE cli path
        ide_cli = config.get('Minitest path', 'ide_cli')
        if miniapp_dict and query_dir and ide_cli:
            print("[*]The configuration has been set.")
            # set configuration to global
            gl.set_value('miniapp_dict', miniapp_dict)
            gl.set_value('query_dir', query_dir)
            gl.set_value('ide_cli', ide_cli)
            gl.set_value("dec_dir", dec_dir)
            gl.set_value('platform', args.platform)
            gl.set_value('source_platform', args.source)
            gl.set_value('decrypted_only_flag', args.justdecrypted)
            return True
        else:
            print("[!]Some values may be empty. Please check your config.ini :/")
            exit(1)
    except:
        print("[!]Missing value of the configuration. Please check your config.ini :/")
        exit(1)


def welcome_info():
    print("[*]Welcome to MiniCAT:MiniCSRF Analysis Tool")
    ascii_art = """\
    ___  ___ _         _  _____   ___  _____ 
    |  \/  |(_)       (_)/  __ \ / _ \|_   _|
    | .  . | _  _ __   _ | /  \// /_\ \ | |  
    | |\/| || || '_ \ | || |    |  _  | | |  
    | |  | || || | | || || \__/\| | | | | |  
    \_|  |_/|_||_| |_||_| \____/\_| |_/ \_/  
    """

    cat = """\
    
      /\_/\                                            
    >( o.o )<                              
     (> ^ <)                                        
    (")\""(")
        |
    """

    for line1, line2 in zip(ascii_art.split('\n'), cat.split('\n')):
        print(line1 + ' ' * 10 + line2)



'''def run_program():
    welcome_info()
    read_ini()
    codeql_query.MiniCSRF_detect.miniCSRF_detect()

if __name__ == '__main__':
    threads = []
    for i in range(5):
        t = threading.Thread(target=run_program)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()'''

# Press the green button in the gutter to run the script.
def main():
    # print(miniapp_dict, query_dir, ide_cli)
    #gl.set_value("log_file", 'run_query.log')
    welcome_info()
    read_ini()
    #copy from raw minicsrf_query
    miniapp_dict = gl.get_value("miniapp_dict")
    query_dir = gl.get_value("query_dir")
    #ide_cli = gl.get_value("ide_cli")
    #gl.set_value("dec_dir",query_dir+"/dec_dir")
    dec_dir = gl.get_value("dec_dir")
    gl.set_value("res_dir",query_dir+"/res")
    #appid_list = []
    not_empty = False
    #for sub_dir in dirs:
    codeql_query.MiniCSRF_detect.miniCSRF_detect(miniapp_dict,query_dir,dec_dir,not_empty,args.appid)
    '''
    dirs = os.listdir(miniapp_dict)
    miniapp_dict = gl.get_value("miniapp_dict")
    if dirs is None:
        print("Nothing in your miniapp_dict,Please check your config file.")
        exit(1)
    print(dirs)
    ...
    for sub_dir in dirs:
    
    '''

if __name__ == '__main__':
    # 解析命令行参数
    args = parser.parse_args()
    # 调用主程序
    main()