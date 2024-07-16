# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import re
import utility.globalvar as gl
import os
import subprocess
import csv
import shutil
import requests

# openai_key = "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"

def path_remake(path):
    return path.replace('\\', '/')

def getFilepath(location_str):
    #split_list = location_str.split("@")
    #fix:if @ in the file path
    split_list = location_str.rsplit('|',1)
    filepath = split_list[0]
    return filepath

def parse_location(location_str):
    #split_list = location_str.split("@")
    #fix:if @ in the file path
    split_list = location_str.rsplit('|',1)
    filepath = split_list[0]
    print(filepath,split_list)
    loc_info = split_list[1].split(":")
    #print(loc_info)
    start_line = int(loc_info[0])
    start_column = int(loc_info[1])
    end_line = int(loc_info[2])
    end_column = int(loc_info[3])
    return (getContent(filepath,start_line,start_column,end_line,end_column))


def getContent(filepath,start_line,start_column,end_line,end_column):
    try:
        des_file = open(filepath,"rb")
        #get the line number of the file.
        current_line = 0
        while current_line < start_line-1:
            des_file.readline()
            current_line += 1
        #read the start_line
        if start_line == end_line:
            tmp_line = des_file.readline()
            tmp_text = tmp_line[start_column-1:end_column]
        #print(str(tmp_text))
        else:
            tmp_line = des_file.readline()
            current_line +=1
            tmp_text = tmp_line[start_column-1:]
            while current_line < end_line:
                tmp_line = des_file.readline()
                current_line +=1
                tmp_text += tmp_line
            if current_line == end_line:
                tmp_line = des_file.readline()
                tmp_text += tmp_line[:end_column-1]
        print(tmp_text.decode('utf-8','ignore'))
        return tmp_text.decode('utf-8','ignore')
    except:
        print("getContent:cannot find the file.Return empty.")
        return ""

def Get_MiddleStr(content, startStr, endStr):  # obtain contents between two strings
    startIndex = content.index(startStr)
    #print(startIndex)
    endIndex = content.index(endStr)
    #print(endIndex)
    if startIndex >= 0:
        startIndex += len(startStr)
        endIndex = content.index(endStr)
    return content[startIndex:endIndex].split(',')

def Get_MiddleStr_only(content, startStr, endStr):  # obtain contents between two strings
    startIndex = content.index(startStr)
    #print(startIndex)
    endIndex = content.index(endStr)
    #print(endIndex)
    if startIndex >= 0:
        startIndex += len(startStr)
        endIndex = content.index(endStr)
    return content[startIndex:endIndex]


# obtain contents between two strings
def Get_MiddleStr_plugin(content, startStr, endStr):
    startIndex = content.index(startStr)
    if startIndex >= 0:
        startIndex += len(startStr)
        endIndex = content.index(endStr)
    return content[startIndex:endIndex]


def delete_quote(s):
    tmp_list = list(s)
    for i in range(len(s)):
        if s[i] == "," and s[i+1] == "}":
            tmp_list[i] = ""
    s = ''.join(tmp_list)
    return s

def judge_zero(tmp_list):
    #replace wx_appid
    tmp_list[0][0] = 0
    for i in tmp_list[0]:
        if i != 0:
            return True
    return False

def judge_ifduplicate(appid):
    print("[*]Removing duplicate final_res_with domain...")
    res_dir = gl.get_value("res_dir")
    with open(res_dir+"/final_res_with_domain.csv",encoding = "utf-8",errors="ignore") as f:
        if str(appid) in f.read():
            print("[*]duplicated.")
            return False
    return True

def judge_ifduplicateX(appid):
    print("[*]Removing duplicate final_res_with domain...")
    res_dir = gl.get_value("res_dir")
    with open(res_dir+"/final_res_with_domainX.csv",encoding = "utf-8",errors="ignore") as f:
        if str(appid) in f.read():
            print("[*]duplicated.X")
            return False
    return True

#REMOVE all source nodes that do not look like url (may lead to false nagatives?)
def check_url_pattern(sink_str):
    print("[.]Check url pattern:",sink_str)
    #sink_list = [x for x in sink_list if "/pages" in x]
    #print(re.findall("(?=\/).*(?=\?)",sink_str))
    if len(re.findall("(?=\/).*?(?=\?)",sink_str)) > 0:
        print("matches.")
        return sink_str
    else:
        # return None
        return "may not url:"+sink_str

def duplicate_url_check(sink_list):
    print(sink_list)
    independent_url_list = []
    ind_T1_count = 0
    ind_T2_count = 0
    ind_T3_count = 0
    for i in sink_list:
        print("now url list:",independent_url_list)
        tmp_list = re.findall("(?=\/).*(?=\?)",str(i))
        print("now tmp_list:",tmp_list)
        if len(tmp_list) > 0:
            if tmp_list[0] in independent_url_list:
                print("url add before.")
                continue
            else:
                if "_#T1" in str(i):
                    ind_T1_count += 1
                elif "_#T2" in str(i):
                    ind_T2_count += 1
                elif "_#T3" in str(i):
                    ind_T3_count += 1
                else:
                    print("something wrong lol.")
                independent_url_list.append(tmp_list[0])
        else:
            print("not found url?")
            continue
    return len(independent_url_list),ind_T1_count,ind_T2_count,ind_T3_count

#count vuln:T1,T2,T3
def vuln_cata(sink_list):
    #print(sink_list)
    T1_count =0
    T2_count =0
    T3_count =0
    for i in sink_list:
        if "_#T1" in str(i):
            T1_count += 1
        elif "_#T2" in str(i):
            T2_count += 1
        elif "_#T3" in str(i):
            T3_count += 1
        else:
            continue
    return T1_count,T2_count,T3_count

def split_E2A_function(text):
    dollar_index = text.find('$')
    if dollar_index != -1:
        return text[dollar_index+1:]
    else:
        return None


def parse_location_wxml(location_str,wxml_file):
    #split_list = location_str.split("@")
    #fix:if @ in the file path
    split_list = location_str.rsplit('|',1)
    filepath = split_list[0]
    if str(wxml_file) not in filepath:
        print("Not the target WXML file.")
        return None
    print(filepath,split_list)
    loc_info = split_list[1].split(":")
    #print(loc_info)
    start_line = int(loc_info[0])
    start_column = int(loc_info[1])
    end_line = int(loc_info[2])
    end_column = int(loc_info[3])
    return (getContent(filepath,start_line,start_column,end_line,end_column))


def getContent_wxml(filepath,start_line,start_column,end_line,end_column):
    des_file = open(filepath,"rb")
    #get the line number of the file.
    current_line = 0
    while current_line < start_line-1:
        des_file.readline()
        current_line += 1
    #read the start_line
    if start_line == end_line:
        tmp_line = des_file.readline()
        tmp_text = tmp_line[start_column-1:end_column]
    #print(str(tmp_text))
    else:
        tmp_line = des_file.readline()
        current_line +=1
        tmp_text = tmp_line[start_column-1:]
        while current_line < end_line:
            tmp_line = des_file.readline()
            current_line +=1
            tmp_text += tmp_line
        if current_line == end_line:
            tmp_line = des_file.readline()
            tmp_text += tmp_line[:end_column-1]
    print(tmp_text.decode('utf-8','ignore'))
    return tmp_text.decode('utf-8','ignore')