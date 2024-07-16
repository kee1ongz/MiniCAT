# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import utility.dataHandler as dh
import utility.globalvar as gl
import utility.resHandler as rh
import codeql_query.MiniCSRF_query as Mimikyu
import re
import os
import subprocess
import csv
import shutil
import requests
import json
import ast

def is_wx_id_exists_in_csv(csv_file, wx_id):
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == wx_id:
                return True
    return False


#chatgpt version
def convert_to_csv(final_list, wx_id, wxml_query_dbname):
    dec_dir = gl.get_value("dec_dir")
    dec_dir = dec_dir + "/" + wx_id + "_dec/"
    # TODO: DO NOT RELEASE THIS. Need this dir for dynamic analysis.
    # if os.path.exists(dec_dir):
    #     print("[*]Removing dec_dir,byebye!")
    #     shutil.rmtree(dec_dir)
    #print("[*]complete.")
    res_array = np.array(final_list)
    #print("res_array")
    #print(res_array)
    cov = pd.DataFrame(res_array)
    if cov.empty:
        print("[*]Nothing here. Maybe this applet is safe?")
        return True
    cov.columns = ["sink", "source", "raw_filepath"]  # Add new column "raw_filepath"
    '''
    print(cov)
    cov["source"] = cov["source"].apply(tuple)
    # Merge all sink nodes that have the same source node.
    cov = cov.groupby(cov["source"])["sink"].apply(set).apply(list).reset_index()
    #print(cov)
    cov["source"] = cov["source"].apply(list)
    '''
    # REMOVE all source nodes that do not look like url (may lead to false negatives?)
    cov["sink"] = cov["sink"].apply(dh.check_url_pattern)
    T1_count, T2_count, T3_count = dh.vuln_cata(cov["sink"].tolist())
    cov = cov.fillna(value={"sink": "", "source": "", "raw_filepath": ""})  # Fill NaN values with empty strings
    cov["function"] = ""
    cov["function"] = cov["sink"].apply(dh.split_E2A_function)
    independent_url_count, ind_T1_count, ind_T2_count, ind_T3_count = dh.duplicate_url_check(cov["sink"].tolist())

    # print(independent_url_count,ind_T1_count,ind_T2_count,ind_T3_count)
    # cov = cov.dropna(subset=['source'])
    cov = cov[cov['sink'].map(bool)]
    print("[*]Writing the query result of " + wx_id + "...")
    query_dir = gl.get_value("query_dir")
    final_csv_name = query_dir + "/res/" + wx_id + "_final.csv"
    if any([T1_count, T2_count, T3_count, independent_url_count, ind_T1_count, ind_T2_count, ind_T3_count]):
        cov.to_csv(final_csv_name)
        rh.simplify_csv(final_csv_name)
        func_wxml_json(final_csv_name,wxml_query_dbname)
    else:
        print("[!]Nothing here for this applet.")
        return True
    
    if os.path.exists(query_dir+"/res/final_res.csv"):
        if is_wx_id_exists_in_csv(query_dir + "/res/final_res.csv",wx_id):
            print("[!]wx_id already exists in final_res.csv. Not writing to CSV.")
            return True
        with open(query_dir+"/res/final_res.csv", "a+", newline='') as res_file:
            if wx_id and len(cov) >= 0:
                writer = csv.writer(res_file)
                writer.writerow(
                    [wx_id, len(cov), T1_count, T2_count, T3_count, independent_url_count, ind_T1_count, ind_T2_count,
                     ind_T3_count])
            res_file.close()
    else:
        print("[*]Creating res file.....")
        with open(query_dir+"/res/final_res.csv", "w", newline='') as res_file:
            writer = csv.writer(res_file)
            writer.writerow(
                ["wechat_app_id", "potential_vuln_count", "T1_vuln", "T2_vuln", "T3_vuln", "independent_url_count",
                 "ind_T1_vuln", "ind_T2_vuln", "ind_T3_vuln"])
            if wx_id and len(cov) >= 0:
                # writer = csv.writer(res_file)
                # writer.writerow(["wechat_app_id","potential_vuln_count","T1_vuln","T2_vuln","T3_vuln","independent_url_count","ind_T1_vuln","ind_T2_vuln","ind_T3_vuln"])
                writer.writerow(
                    [wx_id, len(cov), T1_count, T2_count, T3_count, independent_url_count, ind_T1_count, ind_T2_count,
                     ind_T3_count])
            res_file.close()
    return True

def convert_to_csv_baidu(final_list, baidu_id, swan_query_dbname):
    dec_dir = gl.get_value("dec_dir")
    dec_dir = dec_dir + "/" + baidu_id + "_dec/"
    # TODO: DO NOT RELEASE THIS. Need this dir for dynamic analysis.
    # if os.path.exists(dec_dir):
    #     print("[*]Removing dec_dir,byebye!")
    #     shutil.rmtree(dec_dir)
    #print("[*]complete.")
    res_array = np.array(final_list)
    #print("res_array")
    #print(res_array)
    cov = pd.DataFrame(res_array)
    if cov.empty:
        print("[*]Nothing here. Maybe this applet is safe?")
        return True
    cov.columns = ["sink", "source", "raw_filepath"]  # Add new column "raw_filepath"
    '''
    print(cov)
    cov["source"] = cov["source"].apply(tuple)
    # Merge all sink nodes that have the same source node.
    cov = cov.groupby(cov["source"])["sink"].apply(set).apply(list).reset_index()
    #print(cov)
    cov["source"] = cov["source"].apply(list)
    '''
    # REMOVE all source nodes that do not look like url (may lead to false negatives?)
    cov["sink"] = cov["sink"].apply(dh.check_url_pattern)
    T1_count, T2_count, T3_count = dh.vuln_cata(cov["sink"].tolist())
    cov = cov.fillna(value={"sink": "", "source": "", "raw_filepath": ""})  # Fill NaN values with empty strings
    cov["function"] = ""
    cov["function"] = cov["sink"].apply(dh.split_E2A_function)
    independent_url_count, ind_T1_count, ind_T2_count, ind_T3_count = dh.duplicate_url_check(cov["sink"].tolist())

    # print(independent_url_count,ind_T1_count,ind_T2_count,ind_T3_count)
    # cov = cov.dropna(subset=['source'])
    cov = cov[cov['sink'].map(bool)]
    print("[*]Writing the query result of " + baidu_id + "...")
    query_dir = gl.get_value("query_dir")
    final_csv_name = query_dir + "/res/" + baidu_id + "_final.csv"
    if any([T1_count, T2_count, T3_count, independent_url_count, ind_T1_count, ind_T2_count, ind_T3_count]):
        cov.to_csv(final_csv_name)
        rh.simplify_csv(final_csv_name)
        func_swan_json(final_csv_name,swan_query_dbname)
    else:
        print("[!]Nothing here for this applet.")
        return True
    
    if os.path.exists(query_dir+"/res/final_res_baidu.csv"):
        if is_wx_id_exists_in_csv(query_dir + "/res/final_res_baidu.csv",baidu_id):
            print("[!]baidu_id already exists in final_res_baidu.csv. Not writing to CSV.")
            return True
        with open(query_dir+"/res/final_res_baidu.csv", "a+", newline='') as res_file:
            if baidu_id and len(cov) >= 0:
                writer = csv.writer(res_file)
                writer.writerow(
                    [baidu_id, len(cov), T1_count, T2_count, T3_count, independent_url_count, ind_T1_count, ind_T2_count,
                     ind_T3_count])
            res_file.close()
    else:
        print("[*]Creating res file.....")
        with open(query_dir+"/res/final_res_baidu.csv", "w", newline='') as res_file:
            writer = csv.writer(res_file)
            writer.writerow(
                ["baidu_id", "potential_vuln_count", "T1_vuln", "T2_vuln", "T3_vuln", "independent_url_count",
                 "ind_T1_vuln", "ind_T2_vuln", "ind_T3_vuln"])
            if baidu_id and len(cov) >= 0:
                # writer = csv.writer(res_file)
                # writer.writerow(["wechat_app_id","potential_vuln_count","T1_vuln","T2_vuln","T3_vuln","independent_url_count","ind_T1_vuln","ind_T2_vuln","ind_T3_vuln"])
                writer.writerow(
                    [baidu_id, len(cov), T1_count, T2_count, T3_count, independent_url_count, ind_T1_count, ind_T2_count,
                     ind_T3_count])
            res_file.close()
    return True

'''
# Finally: GFY microsh*t lol.
def convert_to_csv(final_list, wx_id):
    dec_dir = gl.get_value("dec_dir")
    dec_dir = dec_dir+"/" + wx_id + "_dec/"
    #TODO:DO NOT RELEASE THIS. Need the dir for dynamic analysis.
    #if os.path.exists(dec_dir):
    #    print("[*]Removing dec_dir,byebye!")
    #    shutil.rmtree(dec_dir)
    print("[*]complete.")
    res_array = np.array(final_list)
    print("res_array")
    print(res_array)
    cov = pd.DataFrame(res_array)
    if cov.empty:
        print("[*]Nothing here.Maybe this applet is safety?")
        return True
    cov.columns = ["sink", "source"]

    #print(cov)
    #cov["source"] = cov["source"].apply(tuple)
    #Merge all sink nodes that have the same source node.
    #cov = cov.groupby(cov["source"])["sink"].apply(set).apply(list).reset_index()
    #print(cov)
    #cov["source"] = cov["source"].apply(list)

    # REMOVE all source nodes that do not look like url (may lead to false negatives?)
    cov["sink"] = cov["sink"].apply(dh.check_url_pattern)
    T1_count, T2_count, T3_count = dh.vuln_cata(cov["sink"].tolist())
    cov = cov.fillna(value={"sink": "", "source": ""})  # 将 sink 和 source 列中的空值填充为 ""
    cov["function"] = ""
    cov["function"] = cov["sink"].apply(dh.split_E2A_function)
    independent_url_count, ind_T1_count, ind_T2_count, ind_T3_count = dh.duplicate_url_check(cov["sink"].tolist())

    # print(independent_url_count,ind_T1_count,ind_T2_count,ind_T3_count)
    # cov = cov.dropna(subset=['source'])
    cov = cov[cov['sink'].map(bool)]
    print("[*]Writing the query result of "+wx_id+"...")
    query_dir = gl.get_value("query_dir")
    final_csv_name = query_dir+"/res/" + wx_id + "_final.csv"
    if any([T1_count, T2_count, T3_count, independent_url_count, ind_T1_count, ind_T2_count, ind_T3_count]):
        cov.to_csv(final_csv_name)
    else:
        print("[!]Nothing here for this applet.")
        return True
    if os.path.exists(query_dir+"/res/final_res.csv"):
        with open(query_dir+"/res/final_res.csv", "a+", newline='') as res_file:
            if wx_id and len(cov) >= 0:
                writer = csv.writer(res_file)
                writer.writerow(
                    [wx_id, len(cov), T1_count, T2_count, T3_count, independent_url_count, ind_T1_count, ind_T2_count,
                     ind_T3_count])
            res_file.close()
    else:
        print("[*]Creating res file.....")
        with open(query_dir+"/res/final_res.csv", "w", newline='') as res_file:
            writer = csv.writer(res_file)
            writer.writerow(
                ["wechat_app_id", "potential_vuln_count", "T1_vuln", "T2_vuln", "T3_vuln", "independent_url_count",
                 "ind_T1_vuln", "ind_T2_vuln", "ind_T3_vuln"])
            if wx_id and len(cov) >= 0:
                # writer = csv.writer(res_file)
                # writer.writerow(["wechat_app_id","potential_vuln_count","T1_vuln","T2_vuln","T3_vuln","independent_url_count","ind_T1_vuln","ind_T2_vuln","ind_T3_vuln"])
                writer.writerow(
                    [wx_id, len(cov), T1_count, T2_count, T3_count, independent_url_count, ind_T1_count, ind_T2_count,
                     ind_T3_count])
            res_file.close()
    return True
'''


#Write the csv with misc info
def write_final_list(appid, nickname, cate, domain_list):
    print("write_final_list:",appid)
    res_dir = gl.get_value("res_dir")
    if os.path.exists(res_dir+"/final_res.csv"):
        raw_res_query = pd.read_csv(res_dir+"/final_res.csv", encoding='unicode_escape')
        print(raw_res_query)
        cod1 = raw_res_query["wechat_app_id"] == appid
        # raw_res_query[cod1]["test"]
        tmp_res_list = np.array(raw_res_query[cod1]).tolist()
        # os.remove("/data/disk_16t_2/zidong/applet_query/res/final_res.csv")

        # rawres_path = "E:\weapp\codeql_test\res\final_res.csv"
    else:
        print("[!]Reuslt not found.")
    # sum res
    if os.path.exists(res_dir+"/final_res_with_domain.csv"):
        with open(res_dir+"/final_res_with_domain.csv", "a+", newline='') as final_vent:
            writer = csv.writer(final_vent)
            if len(domain_list) > 0 and len(tmp_res_list) > 0 and dh.judge_zero(tmp_res_list) and dh.judge_ifduplicate(appid):
                writer.writerow(
                    [appid, nickname, cate, domain_list, tmp_res_list[0][1], tmp_res_list[0][2], tmp_res_list[0][3],
                     tmp_res_list[0][4], tmp_res_list[0][5], tmp_res_list[0][6], tmp_res_list[0][7],
                     tmp_res_list[0][8]])
            final_vent.close()
    else:
        with open(res_dir+"/final_res_with_domain.csv", "w", newline='') as final_vent:
            writer = csv.writer(final_vent)
            writer.writerow(
                ["wx_appid", "nickname", "cate", "domain_list", "potential_vuln_count", "T1_vuln", "T2_vuln", "T3_vuln",
                 "independent_url_count", "ind_T1_vuln", "ind_T2_vuln", "ind_T3_vuln"])
            if len(domain_list) > 0 and len(tmp_res_list) > 0 and dh.judge_zero(tmp_res_list) and dh.judge_ifduplicate(appid):
                writer.writerow(
                    [appid, nickname, cate, domain_list, tmp_res_list[0][1], tmp_res_list[0][2], tmp_res_list[0][3],
                     tmp_res_list[0][4], tmp_res_list[0][5], tmp_res_list[0][6], tmp_res_list[0][7],
                     tmp_res_list[0][8]])
            final_vent.close()
    print("[*]csv file with final reuslts has benn written.:)")
    # remove duplicate:

'''#build funtion-.wxml file json value-set for wechat ide testing
def func_wxml_json(raw_final_res_file):
    print("[*]Building json file...")
    # 打开csv文件并读取数据
    # 打开csv文件并读取数据
    with open(raw_final_res_file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # 初始化一个字典用于存储结果
        result_dict = {}
        for row in csv_reader:
            # 将set中的元素从.js改为.wxml
            filepaths = row['raw_filepath']
            new_filepaths = [filepath[:-2] + 'wxml' for filepath in eval(filepaths)]
            # 构建json键值对
            result_dict[row['function']] = new_filepaths

    # 将结果保存为json文件
    output_file = os.path.splitext(raw_final_res_file)[0] + '.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        #json.dump(result_dict, f)
        json.dump(result_dict, f,indent = 4, separators = (',', ': '))
    return True'''

'''def func_wxml_json(raw_final_res_file,wxml_query_dbname):
    print("[*]Building json file...")
    with open(raw_final_res_file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        result_dict = {}
        for row in csv_reader:
            if 'functi .' in row['function'] or '.js"' in row['function'] or ' ' in row['function']:
                continue
            filepaths = row['raw_filepath']
            new_filepaths = [filepath[:-2] + 'wxml' for filepath in eval(filepaths)]
            for i in new_filepaths:
                if not os.path.exists(i):
                    print("[!]This file path may not exists")
                    continue
                JSON_flag,wxml_res_csv_name = Mimikyu.wxml_query(row['function'],i,wxml_query_dbname)
                if JSON_flag == 0:
                    print("Oops.")
                    continue
            result_dict[row['function']] = new_filepaths
    output_file = os.path.splitext(raw_final_res_file)[0] + '.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_dict, f,indent = 4, separators = (',', ': '))
    return True'''

def remove_deduplicate_wxml_element(csv_path, deduplicate_cols):
    # 读取CSV文件
    df = pd.read_csv(csv_path,encoding='utf-8')
    
    # 根据指定列进行去重
    df['deduplicated'] = False  # 添加一个新列用于标记是否需要去重
    for i, row in df.iterrows():
        if not row['deduplicated']:
            for j, inner_row in df.iterrows():
                if j > i and not inner_row['deduplicated']:
                    content_a = row[deduplicate_cols].replace(' ', '').replace('\n', '')
                    content_b = inner_row[deduplicate_cols].replace(' ', '').replace('\n', '')
                    if content_b in content_a:
                        df.at[j, 'deduplicated'] = True  # 标记需要去重的行
                        print(f"Deduplicating row {j}: {inner_row[deduplicate_cols]}")
    
    # 保留未被标记为需要去重的行
    df = df[~df['deduplicated']]
    
    # 移除标记列
    df = df.drop('deduplicated', axis=1)
    
    # 保存去重后的结果到新的CSV文件
    # deduplicated_csv_path = csv_path.replace('.csv', '_deduplicated.csv')
    # df.to_csv(deduplicated_csv_path, index=False)
    os.remove(csv_path)  # 删除原始文件
    df.to_csv(csv_path, index=False)  # 保存去重后的结果到原始文件路径
    
    print(f"Deduplicated CSV saved to {csv_path}")



def func_wxml_json(raw_final_res_file, wxml_query_dbname):
    break_flag = 0
    #print("[*]Building json file...")

    # 新增列名
    new_column_names = ['wxml_filepath', 'wxml_element', 'js_E2A_flag', 'wxml_E2A_flag']

    with open(raw_final_res_file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        function_list = []
        for r in csv_reader:
            if 'functi .' in r['function'] or '.js"' in r['function'] or ' ' in r['function']:
                continue
            function_list.append(r['function'])
        print("[*]Function list.")
        print(function_list)
    
    with open(raw_final_res_file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # 更新csv文件头
        fieldnames = csv_reader.fieldnames + new_column_names
        output_file = os.path.splitext(raw_final_res_file)[0] + '_new.csv'
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            csv_writer = csv.DictWriter(f, fieldnames)
            csv_writer.writeheader()

            for row in csv_reader:
                now_func = row['function']
                # 满足条件则新增列内容为"NULL"，并跳过此行
                if 'functi .' in row['function'] or '.js"' in row['function'] or ' ' in row['function']:
                    row.update({new_column: 'NULL' for new_column in new_column_names})
                    csv_writer.writerow(row)
                    continue

                page_loading_function_list = [
                    'onLoad','onShow','onReady','onHide','onUnload','onRouteDone','onPullDownRefresh',
                     'onReachBottom','onPageScroll','onResize','onTabItemTap','onSaveExitState'
                    ]

                if row['function'] in page_loading_function_list:
                    row.update({new_column: 'page control function' for new_column in new_column_names})
                    csv_writer.writerow(row)
                    continue
                        

                filepaths = row['raw_filepath']
                new_filepaths = [filepath[:-2] + 'wxml' for filepath in eval(filepaths)]

                for i in new_filepaths:
                    print("debug only,i is:",i)
                    
                    if not os.path.exists(i.replace(".wxml",".html")):
                        # 如果文件路径不存在则新增列内容为"NULL"，并跳出循环
                        row.update({new_column: 'NULL' for new_column in new_column_names})
                        csv_writer.writerow(row)
                        print("[!]This file path may not exist")
                        #break
                        JSON_flag = -1
                        break_flag = 1
                    #if function name equal to those function, this function will be executed when users are loading pages or switching tabs
                    # so it's no need to find wxml element for them. 
                    page_loading_function_list = [
                    'onLoad','onShow','onReady','onHide','onUnload','onRouteDone','onPullDownRefresh',
                     'onReachBottom','onPageScroll','onResize','onTabItemTap','onSaveExitState'
                    ]
                    if not break_flag:
                        JSON_flag, wxml_res_csv_name = Mimikyu.wxml_query(row['function'], i, wxml_query_dbname,function_list)

                    if JSON_flag == 0 or JSON_flag== -1:
                        # 如果JSON_flag等于0则新增列内容为"NULL"，并跳出循环
                        row.update({new_column: 'NULL' for new_column in new_column_names})
                        #then re-update T1 T2 T3
                        csv_writer.writerow(row)
                        print("Not found result.")
                        break

                    remove_deduplicate_wxml_element(wxml_res_csv_name,'target_element_loc')

                    with open(wxml_res_csv_name, mode='r', encoding='utf-8') as wxml_file:
                        print("[*]Reading the wxml query result file:",wxml_res_csv_name)
                        wxml_reader = csv.DictReader(wxml_file)
                        for wxml_row in wxml_reader:
                            # 如果raw_file_path不等于i则跳过此行
                            if wxml_row['raw_file_path'].replace("_copy","") != i.replace(".wxml",".html"):
                                print("not equal:",wxml_row['raw_file_path'],",",i.replace(".wxml",".html"))
                                continue
                            if now_func not in wxml_row['target_element_loc']:
                                print("maybe not target WXML element,skip")
                                continue
                            print("OK NOW WE START ROCK.")
                            if '#T1' in row['sink']:
                                js_E2A_flag = 'T1'
                            elif '#T2' in row['sink']:
                                js_E2A_flag = 'T2'
                            elif '#T3' in row['sink']:
                                js_E2A_flag = 'T3'

                            # 根据target_element_loc的值来确定wxml_E2A_flag的值
                            if 'wx:if' in wxml_row['target_element_loc'] or 'wx:elif' in wxml_row[
                                'target_element_loc'] or 'wx:else' in wxml_row['target_element_loc']:
                                wxml_E2A_flag = 'F1'
                            elif 'wx:for' in wxml_row['target_element_loc'] or 'wx:key' in wxml_row['target_element_loc']:
                                wxml_E2A_flag = 'F2'
                            else:
                                wxml_E2A_flag = 'F3'

                            # 更新新增列的值
                            row.update({'wxml_filepath': str(i),
                                        'wxml_element': wxml_row['target_element_loc'],
                                        'js_E2A_flag': js_E2A_flag,
                                        'wxml_E2A_flag': wxml_E2A_flag})
                            csv_writer.writerow(row)
    return True


def func_swan_json(raw_final_res_file, swan_query_dbname):
    #print("[*]Building json file...")

    # 新增列名
    new_column_names = ['swan_filepath', 'swan_element', 'js_E2A_flag', 'swan_E2A_flag']

    with open(raw_final_res_file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        function_list = []
        for r in csv_reader:
            if 'functi .' in r['function'] or '.js"' in r['function'] or ' ' in r['function']:
                continue
            function_list.append(r['function'])
        print("[*]Function list.")
        print(function_list)
    
    with open(raw_final_res_file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # 更新csv文件头
        fieldnames = csv_reader.fieldnames + new_column_names
        output_file = os.path.splitext(raw_final_res_file)[0] + '_new.csv'
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            csv_writer = csv.DictWriter(f, fieldnames)
            csv_writer.writeheader()

            for row in csv_reader:
                now_func = row['function']
                # 满足条件则新增列内容为"NULL"，并跳过此行
                if 'functi .' in row['function'] or '.js"' in row['function'] or ' ' in row['function']:
                    row.update({new_column: 'NULL' for new_column in new_column_names})
                    csv_writer.writerow(row)
                    continue

                page_loading_function_list = [
                    'onLoad','onShow','onReady','onHide','onUnload'
                    ]

                if row['function'] in page_loading_function_list:
                    row.update({new_column: 'page control function' for new_column in new_column_names})
                    csv_writer.writerow(row)
                    continue
                        

                filepaths = row['raw_filepath']
                new_filepaths = [filepath[:-2] + 'swan' for filepath in eval(filepaths)]

                for i in new_filepaths:
                    print("debug only,i is:",i)
                    
                    if not os.path.exists(i.replace(".swan",".html")):
                        # 如果文件路径不存在则新增列内容为"NULL"，并跳出循环
                        row.update({new_column: 'NULL' for new_column in new_column_names})
                        csv_writer.writerow(row)
                        print("[!]This file path may not exist")
                        break
                    #if function name equal to those function, this function will be executed when users are loading pages or switching tabs
                    # so it's no need to find wxml element for them. 
                    page_loading_function_list = [
                    'onLoad','onShow','onReady','onHide','onUnload'
                    ]

                    JSON_flag, wxml_res_csv_name = Mimikyu.swan_query(row['function'], i, swan_query_dbname,function_list)

                    if JSON_flag == 0:
                        # 如果JSON_flag等于0则新增列内容为"NULL"，并跳出循环
                        row.update({new_column: 'NULL' for new_column in new_column_names})
                        #then re-update T1 T2 T3
                        csv_writer.writerow(row)
                        print("Not found result.")
                        break

                    remove_deduplicate_wxml_element(wxml_res_csv_name,'target_element_loc')

                    with open(wxml_res_csv_name, mode='r', encoding='utf-8') as wxml_file:
                        print("[*]Reading the swan query result file:",wxml_res_csv_name)
                        wxml_reader = csv.DictReader(wxml_file)
                        for wxml_row in wxml_reader:
                            # 如果raw_file_path不等于i则跳过此行
                            if wxml_row['raw_file_path'].replace("_copy","") != i.replace(".swan",".html"):
                                print("not equal:",wxml_row['raw_file_path'],",",i.replace(".swan",".html"))
                                continue
                            if now_func not in wxml_row['target_element_loc']:
                                print("maybe not target swan element,skip")
                                continue
                            print("OK NOW WE START ROCK.")
                            if '#T1' in row['sink']:
                                js_E2A_flag = 'T1'
                            elif '#T2' in row['sink']:
                                js_E2A_flag = 'T2'
                            elif '#T3' in row['sink']:
                                js_E2A_flag = 'T3'

                            # 根据target_element_loc的值来确定wxml_E2A_flag的值
                            if 's-if' in wxml_row['target_element_loc'] or 's-elif' in wxml_row[
                                'target_element_loc'] or 's-else' in wxml_row['target_element_loc']:
                                swan_E2A_flag = 'F1'
                            elif 's-for' in wxml_row['target_element_loc']:
                                swan_E2A_flag = 'F2'
                            else:
                                swan_E2A_flag = 'F3'

                            # 更新新增列的值
                            row.update({'swan_filepath': str(i),
                                        'swan_element': wxml_row['target_element_loc'],
                                        'js_E2A_flag': js_E2A_flag,
                                        'swan_E2A_flag': swan_E2A_flag})
                            csv_writer.writerow(row)
    return True

def remove_redundant(wxid):
    res_dir = gl.get_value("res_dir")  # res_dir为目标文件夹
    new_dir = res_dir+"/"+wxid+"_res_collect"  # 新建目录名
    os.makedirs(new_dir, exist_ok=True)  # 如果目录不存在，就创建一个
    files = os.listdir(res_dir)  # 获取res_dir下所有文件

    for filename in files:
        if os.path.isdir(os.path.join(res_dir, filename)):  # 如果 filepath 是目录则跳过
            continue
        if filename.startswith(wxid) and filename != f'{wxid}_final_new_X.csv':
            # 如果是以wxid开头，但不是wxid_final_new.csv，则移动到新建目录下
            filepath = os.path.join(res_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'a') as f:
                    f.close()
            shutil.move(filepath, os.path.join(new_dir, filename))



def session_check(raw_final_new, session_check_res):
    # 读取 csv 文件为 pandas DataFrame
    raw_final_new_df = pd.read_csv(raw_final_new)
    session_check_res_df = pd.read_csv(session_check_res)

    # 定义自定义函数
    def check_session_file_path(wxml_filepath):
        # 将 wxml 文件路径替换为 js 文件路径
        js_filepath = str(wxml_filepath).replace('.wxml', '.js')
        # 判断是否命中 session_file_path 列
        if js_filepath in session_check_res_df['session_file_path'].values:
            return 'S1'
        else:
            return 'S2'
    
    def check_session_file_path_baidu(swan_filepath):
        # 将 wxml 文件路径替换为 js 文件路径
        js_filepath = str(swan_filepath).replace('.swan', '.js')
        # 判断是否命中 session_file_path 列
        if js_filepath in session_check_res_df['session_file_path'].values:
            return 'S1'
        else:
            return 'S2'

    # 添加新列 session_check_flag
    if gl.get_value("platform") == "wechat":
        raw_final_new_df['session_check_flag'] = raw_final_new_df['wxml_filepath'].apply(check_session_file_path)
    elif gl.get_value("platform") == "baidu":
        raw_final_new_df['session_check_flag'] = raw_final_new_df['swan_filepath'].apply(check_session_file_path_baidu)



    # 将处理后的 DataFrame 保存为 csv 文件
    #raw_final_new_df.to_csv(raw_final_new, index=False)

    # 保存结果为csv文件，并根据输入的output_suffix修改文件名
    output_filename = os.path.splitext(raw_final_new)[0] + "_X.csv"
    raw_final_new_df.to_csv(output_filename, index=False)

    return output_filename




def collect_csv_finally(final_new_csv, wx_id):
    # 读取CSV文件到DataFrame
    df = pd.read_csv(final_new_csv,encoding='unicode_escape')
    print("[*]Writing final_csv X version...")
    # 统计各类漏洞数量
    final_vuln_count = len(df)
    T1_count = len(df[df['js_E2A_flag'] == 'T1'])
    T2_count = len(df[df['js_E2A_flag'] == 'T2'])
    T3_count = len(df[df['js_E2A_flag'] == 'T3'])
    F1_count = len(df[df['wxml_E2A_flag'] == 'F1'])
    F2_count = len(df[df['wxml_E2A_flag'] == 'F2'])
    F3_count = len(df[df['wxml_E2A_flag'] == 'F3'])
    S1_count = len(df[df['session_check_flag'] == 'S1'])
    S2_count = len(df[df['session_check_flag'] == 'S2'])

    # 写入CSV文件
    query_dir = gl.get_value("query_dir")
    final_csv_name = query_dir + "/res/" + "final_resX.csv"

    if os.path.exists(final_csv_name):
        # CSV文件已经存在，读取现有数据到DataFrame
        result_df = pd.read_csv(final_csv_name)
        if wx_id in result_df['wechat_app_id'].values:
            print("exists,appid:",wx_id)
            return True
    else:
        # CSV文件不存在，创建DataFrame并写入列头
        result_df = pd.DataFrame(
            columns=["wechat_app_id", "potential_vuln_count", "T1_count", "T2_count", "T3_count", "F1_count",
                     "F2_count", "F3_count", "S1_count", "S2_count"])

    # 添加新行
    new_row = {"wechat_app_id": wx_id,
               "potential_vuln_count": final_vuln_count,
               "T1_count": T1_count,
               "T2_count": T2_count,
               "T3_count": T3_count,
               "F1_count": F1_count,
               "F2_count": F2_count,
               "F3_count": F3_count,
               "S1_count": S1_count,
               "S2_count": S2_count}
    result_df = result_df.append(new_row, ignore_index=True)

    # 写入CSV文件
    result_df.to_csv(final_csv_name, index=False)

def collect_csv_finally_baidu(final_new_csv, baidu_id):
    # 读取CSV文件到DataFrame
    df = pd.read_csv(final_new_csv,encoding='unicode_escape')
    print("[*]Writing final_csv X version...")
    # 统计各类漏洞数量
    final_vuln_count = len(df)
    T1_count = len(df[df['js_E2A_flag'] == 'T1'])
    T2_count = len(df[df['js_E2A_flag'] == 'T2'])
    T3_count = len(df[df['js_E2A_flag'] == 'T3'])
    F1_count = len(df[df['swan_E2A_flag'] == 'F1'])
    F2_count = len(df[df['swan_E2A_flag'] == 'F2'])
    F3_count = len(df[df['swan_E2A_flag'] == 'F3'])
    S1_count = len(df[df['session_check_flag'] == 'S1'])
    S2_count = len(df[df['session_check_flag'] == 'S2'])

    # 写入CSV文件
    query_dir = gl.get_value("query_dir")
    final_csv_name = query_dir + "/res/" + "final_resX_baidu.csv"

    if os.path.exists(final_csv_name):
        # CSV文件已经存在，读取现有数据到DataFrame
        result_df = pd.read_csv(final_csv_name)
        if baidu_id in result_df['baidu_id'].values:
            print("exists,appid:",baidu_id)
            return True
    else:
        # CSV文件不存在，创建DataFrame并写入列头
        result_df = pd.DataFrame(
            columns=["baidu_id", "potential_vuln_count", "T1_count", "T2_count", "T3_count", "F1_count",
                     "F2_count", "F3_count", "S1_count", "S2_count"])

    # 添加新行
    new_row = {"baidu_id": baidu_id,
               "potential_vuln_count": final_vuln_count,
               "T1_count": T1_count,
               "T2_count": T2_count,
               "T3_count": T3_count,
               "F1_count": F1_count,
               "F2_count": F2_count,
               "F3_count": F3_count,
               "S1_count": S1_count,
               "S2_count": S2_count}
    result_df = result_df.append(new_row, ignore_index=True)

    # 写入CSV文件
    result_df.to_csv(final_csv_name, index=False)


def write_final_list_X(appid, nickname, cate, domain_list):
    print("write_final_listX:", appid)
    res_dir = gl.get_value("res_dir")
    if os.path.exists(res_dir + "/final_resX.csv"):
        raw_res_query = pd.read_csv(res_dir + "/final_resX.csv", encoding='unicode_escape')
        print(raw_res_query)
        cod1 = raw_res_query["wechat_app_id"] == appid
        # raw_res_query[cod1]["test"]
        tmp_res_list = np.array(raw_res_query[cod1]).tolist()
        # os.remove("/data/disk_16t_2/zidong/applet_query/res/final_res.csv")

        # rawres_path = "E:\weapp\codeql_test\res\final_res.csv"
    else:
        print("[!]Reuslt not found.")
    # sum res
    if os.path.exists(res_dir + "/final_res_with_domainX.csv"):
        with open(res_dir + "/final_res_with_domainX.csv", "a+", newline='') as final_vent:
            writer = csv.writer(final_vent)
            if len(domain_list) > 0 and len(tmp_res_list) > 0 and dh.judge_zero(tmp_res_list) and dh.judge_ifduplicateX(
                    appid):
                writer.writerow(
                    [appid, nickname, cate, domain_list, tmp_res_list[0][1], tmp_res_list[0][2], tmp_res_list[0][3],
                     tmp_res_list[0][4], tmp_res_list[0][5], tmp_res_list[0][6], tmp_res_list[0][7],
                     tmp_res_list[0][8],tmp_res_list[0][9]])
            final_vent.close()
    else:
        with open(res_dir + "/final_res_with_domainX.csv", "w", newline='') as final_vent:
            writer = csv.writer(final_vent)
            writer.writerow(
                ["wx_appid", "nickname", "cate", "domain_list", "potential_vuln_count", "T1_count", "T2_count", "T3_count", "F1_count",
                     "F2_count", "F3_count", "S1_count", "S2_count"])
            if len(domain_list) > 0 and len(tmp_res_list) > 0 and dh.judge_zero(tmp_res_list) and dh.judge_ifduplicateX(
                    appid):
                writer.writerow(
                    [appid, nickname, cate, domain_list, tmp_res_list[0][1], tmp_res_list[0][2], tmp_res_list[0][3],
                     tmp_res_list[0][4], tmp_res_list[0][5], tmp_res_list[0][6], tmp_res_list[0][7],
                     tmp_res_list[0][8],tmp_res_list[0][9]])
            final_vent.close()
    print("[*]csv file with final domain X has benn written.:)")


def remove_dec_dir(dec_dir):
    print("[*]Removing dec_dir...for this round.")
    """
    删除指定目录下的所有文件和目录（包括子目录中的文件和目录）
    """
    # 判断目录是否存在
    if not os.path.exists(dec_dir):
        return

    # 遍历目录中的所有文件和目录，并递归删除
    for root, dirs, files in os.walk(dec_dir, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            os.remove(file_path)
        for name in dirs:
            dir_path = os.path.join(root, name)
            shutil.rmtree(dir_path)

    # 删除最外层目录
    shutil.rmtree(dec_dir)


def time_to_csv(appid, cost_time):
    # Print debug information
    print(f"Writing data: appid={appid}, cost_time={cost_time}")
    res_dir = gl.get_value("res_dir")
    # Define file path and headers
    file_path = res_dir+"/time_sum.csv"
    headers = ["appid", "cost_time"]
    # Check if file exists
    file_exists = os.path.isfile(file_path)

    # Open file and write data
    with open(file_path, mode="a", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)

        # Write headers if file doesn't exist
        if not file_exists:
            writer.writeheader()

        # Write data
        writer.writerow({"appid": appid, "cost_time": cost_time})

        # Print debug information
        print(f"Data written: {appid}, {cost_time}")


#collect decrypted
def decrypted_summary(appid):
    # Print debug information
    print(f"Decrypted Writing data: appid={appid}")


    # Define file path
    res_dir = gl.get_value("res_dir")
    # Define file path and headers
    file_path = res_dir + "/can_be_decrypted.txt"

    if not os.path.exists(file_path):
        open(file_path, 'w').close()

    with open(file_path, mode="r") as file:
        existing_appids = file.read().splitlines()
    
    if appid in existing_appids:
        print(f"appid {appid} already exists in the file. Skipping write operation.")
        return

    # Open file and write data
    with open(file_path, mode="a") as file:
        # Write data
        file.write(f"{appid}\n")

        # Print debug information
        print(f"Data written: {appid}")


def analyzed_summary(appid):
    # Print debug information
    print(f"Analyzed data: appid={appid}")

    # Define file path
    res_dir = gl.get_value("res_dir")
    # Define file path and headers
    if gl.get_value("platform") == "wehcat":
        file_path = res_dir + "/analyzed_applet.txt"
    elif gl.get_value("platform") == "baidu":
        file_path = res_dir + "/analyzed_applet_baidu.txt"
    else:
        file_path = res_dir + "/analyzed_applet.txt"
    
    if not os.path.exists(file_path):
        open(file_path, 'w').close()

    # Check if appid already exists in the file
    with open(file_path, mode="r") as file:
        existing_appids = file.read().splitlines()
    
    if appid in existing_appids:
        print(f"appid {appid} already exists in the file. Skipping write operation.")
        return

    # Open file and write data
    with open(file_path, mode="a") as file:
        # Write data
        file.write(f"{appid}\n")

        # Print debug information
        print(f"Data written: {appid}")

def potential_obfuscation(appid):
    # Print debug information
    print(f"potential_obfuscation: appid={appid}")

    # Define file path
    res_dir = gl.get_value("res_dir")
    # Define file path and headers
    file_path = res_dir + "/potential_obfuscated_applet.txt"

    if not os.path.exists(file_path):
        open(file_path, 'w').close()

    # Check if appid already exists in the file
    with open(file_path, mode="r") as file:
        existing_appids = file.read().splitlines()
    
    if appid in existing_appids:
        print(f"appid {appid} already exists in the file. Skipping write operation.")
        return

    # Open file and write data
    with open(file_path, mode="a") as file:
        # Write data
        file.write(f"{appid}\n")

        # Print debug information
        print(f"Data written: {appid}")

def decrypted_failed(appid):
    # Print debug information
    print(f"decrypted_failed: appid={appid}")

    # Define file path
    res_dir = gl.get_value("res_dir")
    # Define file path and headers
    file_path = res_dir + "/decrypted_failed_applet.txt"

    if not os.path.exists(file_path):
        open(file_path, 'w').close()

    # Check if appid already exists in the file
    with open(file_path, mode="r") as file:
        existing_appids = file.read().splitlines()
    
    if appid in existing_appids:
        print(f"appid {appid} already exists in the file. Skipping write operation.")
        return

    # Open file and write data
    with open(file_path, mode="a") as file:
        # Write data
        file.write(f"{appid}\n")

        # Print debug information
        print(f"Data written: {appid}")

