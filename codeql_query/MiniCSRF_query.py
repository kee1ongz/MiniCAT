# -*- coding:utf-8 -*-
import platform
import utility.globalvar as gl
import utility.resHandler as rh
import utility.dataHandler as dh
import utility.output as op
import pandas as pd
import numpy as np
import re
import os
import subprocess
import csv
import shutil
import requests
import time
import signal
import traceback
import psutil

class QueryRunTimeoutError(Exception):
    pass


def create_database(source_code_root_path):
    # source code -> ql_db
    cmd = "codeql database create {}_db --language=javascript --threads=32".format(
         source_code_root_path)
    os.system(cmd)
    #subprocess.run(cmd, shell=True, check=True)

'''
def query_run(ql_db_path, ql_query, bqrs_path):
    appid = gl.get_value("appid")
    cmd = "codeql query run {} --database={} --output={} --threads=32 --timeout=50".format(
        ql_query, ql_db_path, bqrs_path)
    process = subprocess.Popen(cmd, shell=True)
    try:
        process.communicate(timeout=100)
    except subprocess.TimeoutExpired:
        # Get the PID of the process after timeout
        pid = process.pid
        print("maybe timeout,the query pid is:",pid)
        # Terminate the process using psutil
        process = psutil.Process(pid)
        process.terminate()
        process.wait(timeout=5)
        
        # If the process is still running, force kill it
        if process.is_running():
            print("still running")
            process.kill()
            process.wait()
        # 超时后终止进程
        op.potential_obfuscation(appid)
        print("Command execution timed out")
'''

def query_run(ql_db_path, ql_query, bqrs_path):
    appid = gl.get_value("appid")
    cmd = "codeql query run {} --database={} --output={} --threads=32 --timeout=60".format(
        ql_query, ql_db_path, bqrs_path)
    #process = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        # 执行命令并设置超时时间为300秒
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        # 获取命令执行后的标准输出和标准错误
        stdout = result.stdout
        stderr = result.stderr
        
        # 检查回显中是否包含"[1/1 timeout"
        if "timeout" in stdout or "timeout" in stderr:
            # 进一步处理，例如打印错误信息或执行其他操作
            print("query Timeout occurred.")
            op.potential_obfuscation(appid)
            raise subprocess.TimeoutExpired
    except subprocess.TimeoutExpired:
        # Get the PID of the process after timeout
        pid = process.pid
        print("maybe timeout,the query pid is:",pid)
        # Terminate the process using psutil
        process = psutil.Process(pid)
        process.terminate()
        process.wait(timeout=5)
        
        # If the process is still running, force kill it
        if process.is_running():
            print("still running")
            process.kill()
            process.wait()
        # 超时后终止进程
        op.potential_obfuscation(appid)
        print("Command execution timed out")


def decode_bqrs(bqrs_path, output_csv_path, result_set):
    # bqrs -> csv
    cmd = "codeql bqrs decode  {} --format=csv --result-set={} --output={}".format(
        bqrs_path, result_set, output_csv_path)
    os.system(cmd)
    #subprocess.run(cmd, shell=True)


def wxml_to_html_convert(raw_dec_dir,wx_id):
    #gl.set_value("raw_wxml_func_name_tmp", "hi")
    now_dir = os.getcwd()
    print("[*]Preparing for the wxml analysis.")
    # 创建新目录并复制文件
    # new_dir = raw_dec_dir + "_copy"
    # if os.path.exists(new_dir):
    #     return raw_dec_dir + "_copy/" + wx_id + "_wxml_db"
    # shutil.copytree(raw_dec_dir, new_dir)
    new_dir = raw_dec_dir

    # 对.wxml文件更改后缀为.html
    for root, dirs, files in os.walk(new_dir):
        for file in files:
            if file.endswith(".wxml"):
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, os.path.splitext(file)[0] + ".html")
                os.rename(old_path, new_path)

    # 切换工作目录并传入参数
    os.chdir(new_dir)
    print("[*]Creating .wxml codeQL database...")
    create_database(wx_id+"_wxml")
    os.chdir(now_dir)
    return raw_dec_dir + "/"+wx_id+"_wxml_db"
    # return raw_dec_dir + "_copy/"+wx_id+"_wxml_db"


def swan_to_html_convert(raw_dec_dir,baidu_id):
    #gl.set_value("raw_wxml_func_name_tmp", "hi")
    now_dir = os.getcwd()
    print("[*]Preparing for the swan analysis.")
    # 创建新目录并复制文件
    # new_dir = raw_dec_dir + "_copy"
    # if os.path.exists(new_dir):
    #     return raw_dec_dir + "_copy/" + wx_id + "_wxml_db"
    # shutil.copytree(raw_dec_dir, new_dir)
    new_dir = raw_dec_dir

    # 对.wxml文件更改后缀为.html
    for root, dirs, files in os.walk(new_dir):
        for file in files:
            if file.endswith(".swan"):
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, os.path.splitext(file)[0] + ".html")
                os.rename(old_path, new_path)

    # 切换工作目录并传入参数
    os.chdir(new_dir)
    print("[*]Creating .swan codeQL database...")
    create_database(baidu_id+"_swan")
    os.chdir(now_dir)
    return raw_dec_dir + "/"+baidu_id+"_swan_db"
    # return raw_dec_dir + "_copy/"+wx_id+"_wxml_db"


def extract_between_percentages(target_string):
    match = re.search(r'%([^%]+)%', target_string)
    if match:
        return match.group(1)
    else:
        return None

def replace_target_attr(source_func_name,query_file_path):
    if os.stat(query_file_path).st_size == 0:
        print("wxml query is empty,use bakup.")
        with open(gl.get_value("query_dir")+"/codeql_query/ql_starter/codeql-custom-queries-javascript/wxml_query_bak.ql", 'r') as b_file:
            b_content = b_file.read()
        # 将文件 B 的内容写入文件 A
        with open(query_file_path, 'w') as a_file:
            a_file.write(b_content)
            print("[*]Rewriting wxml_query.ql done.")

    #raw_wxml_func_name_tmp = gl.get_value("raw_wxml_func_name_tmp")
    print("[@@]Replacing query function:",source_func_name)
    with open(query_file_path, 'r') as f:
        content = f.read()
    gl.set_value("raw_wxml_func_name_tmp",extract_between_percentages(content))
    raw_wxml_func_name_tmp = gl.get_value("raw_wxml_func_name_tmp")
    new_content = content.replace(f'%{raw_wxml_func_name_tmp}%', f'%{source_func_name}%')
    gl.set_value("raw_wxml_func_name_tmp",source_func_name)
    with open(query_file_path, 'w') as f:
        f.write(new_content)
    f.close()
    print("Rewriting done.")

def all_function_replace_target_attr(function_list,query_file_path):
    #raw_wxml_func_name_tmp = gl.get_value("raw_wxml_func_name_tmp")
    print("[@@]ALL FUNTION IN.")
    # with open(query_file_path, 'r') as f:
    #     content = f.read()
    # target_string = 'string target_function()\n{\n  result = "%hi%"'
    # function_list = list(set(function_list))
    # function_names = [f'%{name}%' for name in function_list]
    # with open(query_file_path, 'r+') as file:
    #     content = file.read()
    #     index = content.find(target_string)

    #     if index != -1:
    #         insert_index = index + len(target_string)
    #         file.seek(insert_index)
    #         file.write(''.join([f' or result="{name}"' for name in function_names]))

    #         print("Functions added successfully!")
    #         file.close()
    #     else:
    #         print("Target function not found in the file.")
    target_string = 'result = "%hi%"'
    function_list = list(set(function_list))
    function_names = [f'or\nresult = "%{name}%"\n' for name in function_list]
    with open(query_file_path, 'r+') as file:
        lines = file.readlines()
        index = -1

        # 寻找目标字符串的行索引
        for i, line in enumerate(lines):
            if target_string in line:
                index = i
                break

        if index != -1:
            insert_index = index + 1
            lines = lines[:insert_index] + function_names + lines[insert_index:]

            file.seek(0)
            file.writelines(lines)
            file.truncate()

            print("Functions added successfully!")
        else:
            print("Target function not found in the file.")

    
    # gl.set_value("raw_wxml_func_name_tmp",extract_between_percentages(content))
    # raw_wxml_func_name_tmp = gl.get_value("raw_wxml_func_name_tmp")
    # new_content = content.replace(f'%{raw_wxml_func_name_tmp}%', f'%{source_func_name}%')
    # gl.set_value("raw_wxml_func_name_tmp",source_func_name)
    # with open(query_file_path, 'w') as f:
    #     f.write(new_content)
    # f.close()
    # print("Rewriting done.")   


def wxml_query(function_name,wxml_file_path,wxml_query_dbname,function_list):
    file_a = gl.get_value("query_dir")+"/codeql_query/ql_starter/codeql-custom-queries-javascript/wxml_query_reborn.ql"
    file_b = gl.get_value("query_dir")+"/codeql_query/ql_starter/codeql-custom-queries-javascript/wxml_query_reborn_bak.ql"
    with open(file_a, 'r') as f_a:
        content_a = f_a.read()
        f_a.close()

    with open(file_b, 'r') as f_b:
        content_b = f_b.read()
        f_b.close()

    if content_a != content_b:
        with open(file_a, 'w') as file_a:
            file_a.write(content_b)
        print("File content replaced.")
    else:
        print("File contents are the same.")

    before_pwd = os.getcwd()
    source_path = gl.get_value("source_path")
    os.chdir(source_path)
    JSON_flag = 1
    #query_file_path = gl.get_value("query_dir")+"/codeql_query/ql_starter/codeql-custom-queries-javascript/wxml_query.ql"
    reborn_query_file_path = gl.get_value("query_dir")+"/codeql_query/ql_starter/codeql-custom-queries-javascript/wxml_query_reborn.ql"
    #tmp_wxml_query_file_path = gl.get_value("query_dir")+"/codeql_query/ql_starter/codeql-custom-queries-javascript/wxml_query"+str(function_name)+".ql"
    # replace_target_attr(function_name,query_file_path)
    # query_run(wxml_query_dbname,query_file_path,gl.get_value("appid")+"_wxml.bqrs")
    # #decode_bqrs(gl.get_value("appid")+"_wxml.bqrs", gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_"+function_name+".csv", "wxml_get_function")
    # decode_bqrs(gl.get_value("appid")+"_wxml.bqrs", gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_"+function_name+".csv", "wxml_get_function_loc")
    
    if os.path.exists(gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_wxml_all.csv"):
        print("WXML queried before.")
        os.chdir(before_pwd)
        return JSON_flag,gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_wxml_all.csv"
    else:
        print("[*]Rewriting the query script.")
        all_function_replace_target_attr(function_list,reborn_query_file_path)
        query_run(wxml_query_dbname,reborn_query_file_path,gl.get_value("appid")+"_wxml_all.bqrs")
        decode_bqrs(gl.get_value("appid")+"_wxml_all.bqrs", 
                gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_wxml_all.csv", 
                "wxml_get_function_loc")
    # if rh.check_csv_header_only(gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_"+function_name+".csv"):
    #     print("[!]No result.")
    #     os.remove(gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_"+function_name+".csv")
    #     JSON_flag = 0
    #     return JSON_flag,None
    
    if rh.check_csv_header_only(gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_wxml_all.csv"):
        print("[!]No result.")
        os.remove(gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_wxml_all.csv")
        JSON_flag = 0
        return JSON_flag,None
    
    #wxml_res_csv_name = rh.result_cleaning_for_wxml(gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_"+function_name+".csv",wxml_file_path)

    wxml_res_csv_name = rh.result_cleaning_for_wxml(gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_wxml_all.csv")
    os.chdir(before_pwd)
    return JSON_flag,wxml_res_csv_name
    #query_run(wx_id+"_db",query_path,wx_id+".bqrs")

def swan_query(function_name,wxml_file_path,wxml_query_dbname,function_list):
    file_a = gl.get_value("query_dir")+"/codeql_query/ql_starter/codeql-custom-queries-javascript/swan_query_reborn.ql"
    file_b = gl.get_value("query_dir")+"/codeql_query/ql_starter/codeql-custom-queries-javascript/swan_query_reborn_bak.ql"
    with open(file_a, 'r') as f_a:
        content_a = f_a.read()
        f_a.close()

    with open(file_b, 'r') as f_b:
        content_b = f_b.read()
        f_b.close()

    if content_a != content_b:
        with open(file_a, 'w') as file_a:
            file_a.write(content_b)
        print("File content replaced.")
    else:
        print("File contents are the same.")

    before_pwd = os.getcwd()
    source_path = gl.get_value("source_path")
    os.chdir(source_path)
    JSON_flag = 1
    #query_file_path = gl.get_value("query_dir")+"/codeql_query/ql_starter/codeql-custom-queries-javascript/wxml_query.ql"
    reborn_query_file_path = gl.get_value("query_dir")+"/codeql_query/ql_starter/codeql-custom-queries-javascript/wxml_query_reborn.ql"
    #tmp_wxml_query_file_path = gl.get_value("query_dir")+"/codeql_query/ql_starter/codeql-custom-queries-javascript/wxml_query"+str(function_name)+".ql"
    # replace_target_attr(function_name,query_file_path)
    # query_run(wxml_query_dbname,query_file_path,gl.get_value("appid")+"_wxml.bqrs")
    # #decode_bqrs(gl.get_value("appid")+"_wxml.bqrs", gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_"+function_name+".csv", "wxml_get_function")
    # decode_bqrs(gl.get_value("appid")+"_wxml.bqrs", gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_"+function_name+".csv", "wxml_get_function_loc")
    
    if os.path.exists(gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_swan_all.csv"):
        print("SWAN queried before.")
        os.chdir(before_pwd)
        return JSON_flag,gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_swan_all.csv"
    else:
        print("[*]Rewriting the query script.")
        all_function_replace_target_attr(function_list,reborn_query_file_path)
        query_run(wxml_query_dbname,reborn_query_file_path,gl.get_value("appid")+"_swan_all.bqrs")
        decode_bqrs(gl.get_value("appid")+"_swan_all.bqrs", 
                gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_swan_all.csv", 
                "wxml_get_function_loc")
    # if rh.check_csv_header_only(gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_"+function_name+".csv"):
    #     print("[!]No result.")
    #     os.remove(gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_"+function_name+".csv")
    #     JSON_flag = 0
    #     return JSON_flag,None
    
    if rh.check_csv_header_only(gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_swan_all.csv"):
        print("[!]No result.")
        os.remove(gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_swan_all.csv")
        JSON_flag = 0
        return JSON_flag,None
    
    #wxml_res_csv_name = rh.result_cleaning_for_wxml(gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_"+function_name+".csv",wxml_file_path)

    wxml_res_csv_name = rh.result_cleaning_for_wxml(gl.get_value("res_dir") + "/" + gl.get_value("appid") + "_swan_all.csv")
    os.chdir(before_pwd)
    return JSON_flag,wxml_res_csv_name
    #query_run(wx_id+"_db",query_path,wx_id+".bqrs")

def query_session(source_path,wx_id):
    query_dir = gl.get_value("query_dir")
    gl.set_value("res_dir",query_dir+"/res")
    res_dir = query_dir+"/res"
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)
    before_pwd = os.getcwd()
    os.chdir(source_path)
    #create_db = "codeql database create -source-root=E_/weapp/codeql_test/raw_miniapp_wx/test/wxe186e23f5a8f0dbf/test_dec1 "+wx_id+"_db --language=javascript"
    print("[*]Running Session Query...")
    query_path = query_dir+"/codeql_query/ql_starter/codeql-custom-queries-javascript/checkSession.ql"
    query_run(wx_id+"_db",query_path,wx_id+".bqrs")
    print("[*]Bqrs decoding...")
    #Updated：23/04/18,the pred function name has been added.
    print("[*]Writing the session check result...")
    decode_bqrs(wx_id+".bqrs",res_dir+"/" + wx_id+"_sessionCheck.csv","session_check")
    #decode_bqrs(wx_id + ".bqrs", res_dir + "/" + wx_id + ".csv", "get_func")
    os.chdir(before_pwd)
    #print("[*]Removing dic...")
    return res_dir+"/" + wx_id+"_sessionCheck.csv"


def query_wechat(source_path,wx_id):
    query_dir = gl.get_value("query_dir")
    gl.set_value("res_dir",query_dir+"/res")
    res_dir = query_dir+"/res"
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)
    before_pwd = os.getcwd()
    os.chdir(source_path)
    #create_db = "codeql database create -source-root=E_/weapp/codeql_test/raw_miniapp_wx/test/wxe186e23f5a8f0dbf/test_dec1 "+wx_id+"_db --language=javascript"
    print("[*]Creating the CodeQL database...")
    create_database(wx_id)
    print("[*]Running Query...")
    query_path = query_dir+"/codeql_query/ql_starter/codeql-custom-queries-javascript/wechat_query_reborn.ql"
    query_run(wx_id+"_db_all_in_one",query_path,wx_id+".bqrs")
    print("[*]Bqrs decoding...")
    #Updated：23/04/18,the pred function name has been added.
    print("[*]Writing the main query result:pure_get_func..")
    decode_bqrs(wx_id + ".bqrs", res_dir + "/" + wx_id + "_aux.csv", "pure_get_func")
    print("[*]Writing the auxiliary query result:get_func..")
    decode_bqrs(wx_id+".bqrs",res_dir+"/" + wx_id+"_main.csv","get_func")
    print("[*]Processing the source function result...")
    rh.judge_source_function(res_dir + "/" + wx_id + "_main.csv",res_dir+"/" + wx_id+"_aux.csv",wx_id)
    #decode_bqrs(wx_id + ".bqrs", res_dir + "/" + wx_id + ".csv", "get_func")
    os.chdir(before_pwd)
    print("[*]Removing dic...")
    return True


def query_wechat_reborn(source_path,wx_id,wxml_query_dbname):
    query_dir = gl.get_value("query_dir")
    gl.set_value("res_dir",query_dir+"/res")
    res_dir = query_dir+"/res"
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)
    before_pwd = os.getcwd()
    os.chdir(source_path)
    #create_db = "codeql database create -source-root=E_/weapp/codeql_test/raw_miniapp_wx/test/wxe186e23f5a8f0dbf/test_dec1 "+wx_id+"_db --language=javascript"
    # print("[*]Creating the CodeQL database...")
    # create_database(wx_id)
    print("[*]Running Query...")
    query_path = query_dir+"/codeql_query/ql_starter/codeql-custom-queries-javascript/xros_query_for_wxapp.ql"
    query_run(wxml_query_dbname,query_path,wx_id+".bqrs")
    print("[*]Bqrs decoding...")
    #Updated：23/04/18,the pred function name has been added.

    #from raw_query_wechat_reborn
    print("[*]Writing the main query result:pure_get_func..")
    decode_bqrs(wx_id + ".bqrs", res_dir + "/" + wx_id + "_aux.csv", "pure_get_func")
    print("[*]Writing the auxiliary query result:get_func..")
    decode_bqrs(wx_id+".bqrs",res_dir+"/" + wx_id+"_main.csv","get_func")
    print("[*]Processing the source function result...")
    rh.judge_source_function(res_dir + "/" + wx_id + "_main.csv",res_dir+"/" + wx_id+"_aux.csv",wx_id)
    #decode_bqrs(wx_id + ".bqrs", res_dir + "/" + wx_id + ".csv", "get_func")

    #from raw query_session,return res_dir+"/" + wx_id+"_sessionCheck.csv"
    print("[*]Bqrs decoding...")
    #Updated：23/04/18,the pred function name has been added.
    print("[*]Writing the session check result...")
    decode_bqrs(wx_id+".bqrs",res_dir+"/" + wx_id+"_sessionCheck.csv","session_check")
    os.chdir(before_pwd)
    print("[*]Removing dic...")

    #from raw wxml_query
    return res_dir+"/" + wx_id+"_sessionCheck.csv"



def query_baidu_reborn(source_path,baidu_id,wxml_query_dbname):
    query_dir = gl.get_value("query_dir")
    gl.set_value("res_dir",query_dir+"/res")
    res_dir = query_dir+"/res"
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)
    before_pwd = os.getcwd()
    os.chdir(source_path)
    #create_db = "codeql database create -source-root=E_/weapp/codeql_test/raw_miniapp_wx/test/wxe186e23f5a8f0dbf/test_dec1 "+wx_id+"_db --language=javascript"
    # print("[*]Creating the CodeQL database...")
    # create_database(wx_id)
    print("[*]Running Query...")
    query_path = query_dir+"/codeql_query/ql_starter/codeql-custom-queries-javascript/xros_query_for_baidu.ql"
    query_run(wxml_query_dbname,query_path,baidu_id+".bqrs")
    print("[*]Bqrs decoding...")
    #Updated：23/04/18,the pred function name has been added.

    #from raw_query_wechat_reborn
    print("[*]Writing the main query result:pure_get_func..")
    decode_bqrs(baidu_id + ".bqrs", res_dir + "/" + baidu_id + "_aux.csv", "pure_get_func")
    print("[*]Writing the auxiliary query result:get_func..")
    decode_bqrs(baidu_id+".bqrs",res_dir+"/" + baidu_id+"_main.csv","get_func")
    print("[*]Processing the source function result...")
    rh.judge_source_function(res_dir + "/" + baidu_id + "_main.csv",res_dir+"/" + baidu_id+"_aux.csv",baidu_id)
    #decode_bqrs(wx_id + ".bqrs", res_dir + "/" + wx_id + ".csv", "get_func")

    #from raw query_session,return res_dir+"/" + wx_id+"_sessionCheck.csv"
    print("[*]Bqrs decoding...")
    #Updated：23/04/18,the pred function name has been added.
    print("[*]Writing the session check result...")
    decode_bqrs(baidu_id+".bqrs",res_dir+"/" + baidu_id+"_sessionCheck.csv","session_check")
    os.chdir(before_pwd)
    print("[*]Removing dic...")

    #from raw wxml_query
    return res_dir+"/" + baidu_id+"_sessionCheck.csv"

def justCreateDb_BLE(raw_dec_dir,wx_id):
    #gl.set_value("raw_wxml_func_name_tmp", "hi")
    now_dir = os.getcwd()
    print("[*]Preparing for the BLE analysis.")
    # 创建新目录并复制文件
    # new_dir = raw_dec_dir + "_copy"
    # if os.path.exists(new_dir):
    #     return raw_dec_dir + "_copy/" + wx_id + "_wxml_db"
    # shutil.copytree(raw_dec_dir, new_dir)
    new_dir = raw_dec_dir

    # 对.wxml文件更改后缀为.html
    # 切换工作目录并传入参数
    os.chdir(new_dir)
    print("[*]Creating .wxml codeQL database...")
    create_database(wx_id+"_swan")
    os.chdir(now_dir)
    return raw_dec_dir + "/"+wx_id+"_swan_db"
    # return raw_dec_dir + "_copy/"+wx_id+"_wxml_db"

def query_BLE_reborn(source_path,wx_id,BLE_dbname):
    query_dir = gl.get_value("query_dir")
    gl.set_value("res_dir",query_dir+"/res")
    res_dir = query_dir+"/res"
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)
    before_pwd = os.getcwd()
    os.chdir(source_path)
    #create_db = "codeql database create -source-root=E_/weapp/codeql_test/raw_miniapp_wx/test/wxe186e23f5a8f0dbf/test_dec1 "+wx_id+"_db --language=javascript"
    # print("[*]Creating the CodeQL database...")
    # create_database(wx_id)
    print("[*]Running Query...")
    query_path = query_dir+"/codeql_query/ql_starter/codeql-custom-queries-javascript/BLE_node_detector.ql"
    query_run(BLE_dbname,query_path,wx_id+".bqrs")
    print("[*]Bqrs decoding...")
    #Updated：23/04/18,the pred function name has been added.

    #from raw_query_wechat_reborn
    print("[*]Writing the main query result:ifInvoke")
    decode_bqrs(wx_id + ".bqrs", res_dir + "/" + wx_id + "_BLE.csv", "ifInvoke")

    rh.judge_source_function(res_dir + "/" + wx_id + "_main.csv",res_dir+"/" + wx_id+"_aux.csv",wx_id)
    #decode_bqrs(wx_id + ".bqrs", res_dir + "/" + wx_id + ".csv", "get_func")

    #from raw query_session,return res_dir+"/" + wx_id+"_sessionCheck.csv"
    print("[*]Bqrs decoding...")
    #Updated：23/04/18,the pred function name has been added.
    print("[*]Writing the session check result...")
    decode_bqrs(wx_id+".bqrs",res_dir+"/" + wx_id+"_sessionCheck.csv","session_check")
    os.chdir(before_pwd)
    print("[*]Removing dic...")

    #from raw wxml_query
    return res_dir+"/" + wx_id+"_sessionCheck.csv"
