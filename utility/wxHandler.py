import os
import subprocess
import shutil
import minium
import execjs
from js_code import *

def wx_decrypt(appid,tar,path,dec_dir):
    pass
    mini = minium.Minium({
        "project_path": "E:/weapp/oklok1023/_1027500618_45",   # 替换成你的【小程序项目目录地址】
        "dev_tool_path": "D:/微信web开发者工具/cli.bat",      # 替换成你的【开发者工具cli地址】，macOS: <安装路径>/Contents/MacOS/cli， Windows: <安装路径>/cli.bat
    })
    print(mini.get_system_info())


def js_from_file(file_name):
    """
    读取js文件
    :return:
    """
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()

    return result

def wxml_to_html(sourcePath, savePath, options):
    pass





