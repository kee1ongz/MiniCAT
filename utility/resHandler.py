# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import utility.dataHandler as dh
import utility.globalvar as gl
import re
import os
import subprocess
import csv
import shutil
import requests

def judge_share(raw_list, source_path):
    for item in raw_list:
        key = item[0]
        # find url
        test_url = re.findall("(?=\/).*?(?=\?)", key)
        print("[*]test_url:", test_url)
        if len(test_url) == 1:
            filename = source_path + test_url[0] + ".js"
            if os.path.exists(filename):
                with open(filename, "rb") as f:
                    tmp_content = f.read()
                    if b"onShareAppMessage" in tmp_content:
                        print("[*]bingo:", test_url[0], ".js is vulnerable.")
                    else:
                        print("[!]maybe unavailable")
                        item = ("NO_SHARED", item[1], item[2])
            else:
                print("file not found.")
                item = ("Null", item[1], item[2])
    judge_res_list = [y for y in raw_list if y[0] != "Null"]
    print("judge_res:", judge_res_list)
    return judge_res_list
'''
def judge_share(raw_list,source_path):
    #print("raw_list:",raw_list)
    #onShareAppMessage
    for key in raw_list:
        #print("key is:",key)
        #print(raw_list[key][0])
        #print("now judging page:",key[0])
        #find url
        #TODO:正则写的有问题，应该是“”之间，pages开头直到，?之前
        
        #raw_url = re.findall("(?<=\").*?(?=\")",key[0])
        #print(raw_url)
        #find_the_page = re.findall("(^.*)(?=\?)",raw_url[0])
        
        #test_url = re.findall("(?=\/pages).*(?=\?)",key[0])
        #Fix: those situations: /abcd/eee/sjsj?a=1
        #print("key[0] is:",key[0])
        test_url = re.findall("(?=\/).*?(?=\?)", key[0])
        print("[*]test_url:",test_url)
        if len(test_url)==1:
            #print("test_url[0],",test_url[0])
            filename=source_path+test_url[0]+".js"
            if os.path.exists(filename):
                with open(filename,"rb") as f:
                    tmp_content = f.read()
                    if b"onShareAppMessage" in tmp_content:
                        print("[*]bingo:",test_url[0],".js is vulnerable.")
                    else:
                        print("[!]maybe unavailable")
                        key[0] = "Null"
            else:
                print("file not found.")
                key[0] = "Null"
    judge_res_list = [y for y in raw_list if y[0] != "Null"]
    #print("judge_res:",judge_res_list)
    return judge_res_list
'''
def judge_set(value_set,tmp_value):
    for i in iter(value_set):
        #print("i is:",i,",and tmp_value:",tmp_value)
        if tmp_value in str(i):
            #print("may be child.")
            if len(str(i)) >len(tmp_value):
                #print("raw is longer.")
                return value_set
            value_set.remove(i)
            value_set.add(tmp_value)
            return value_set
    value_set.add(tmp_value)
    return value_set


def remove_duplicate_list(raw_list):
    #print("raw_list:",raw_list)
    tmp_dicts = dict()
    tmp_value_set = set()
    print("[*]E2A analysis:Adding T* sign and function names..")
    '''
    for key in raw_list:
        #print("key:",key[0],key[1],key[2],key[3])
        if "entry node" in key[2]:
            key[0] += "_#T3$"+key[3]
        elif "is true" in key[2]:
            key[0] += "_#T1$"+key[3]
        elif "is false" in key[2]:
            key[0] += "_#T2$"+key[3]
        else:
            key[0] += "_#T2$"+key[3]
        print("[*]Removing Duplicate rows.")
        if not tmp_dicts.get(key[0],None):
            tmp_value_set = set()
            tmp_value_set.add(key[1])
            tmp_dicts[key[0]] = tmp_value_set
            #print("Tmp_dicts is:",tmp_dicts,",key[0]:",key[0],",key[1]:",key[1])
        else:
            k = tmp_dicts.get(key[0],None)
            #print("in else,Tmp_dicts is:",tmp_dicts,",key[0]:",key[0],",key[1]:",key[1])
            #print("k is:",k)
            if key[1] not in k:
                tmp_value_set=judge_set(k,key[1])
    #print("tmp_dicts:",tmp_dicts)
    #Test:
    res =[[x,y] for x,y in tmp_dicts.items()]
    '''
    #chatgpt version:
    tmp_dicts = dict()
    for key in raw_list:
        if "entry node" in key[2]:
            key0 = key[0] + "_#T3$" + key[3]
        elif "is true" in key[2]:
            key0 = key[0] + "_#T1$" + key[3]
        elif "is false" in key[2]:
            key0 = key[0] + "_#T2$" + key[3]
        else:
            key0 = key[0] + "_#T2$" + key[3]

        if key0 not in tmp_dicts:
            tmp_dicts[key0] = dict()
        if key[1] not in tmp_dicts[key0]:
            tmp_dicts[key0][key[1]] = set()
        tmp_dicts[key0][key[1]].add(key[4])
    res = [(k, v1, v2) for k, v in tmp_dicts.items() for v1, v2 in v.items()]
    print(res)
    return res

def result_cleaning(res_csv_filename,source_path):
    print("[*]Get the res_file:"+res_csv_filename)
    #TODO:remember to release
    print("Rewriting the res csv file...")
    columns = ['sink_loc', 'source_loc', 'block_name', 'source_func']
    #UPGRADED:test_prep
    #columns = ['sink_loc', 'source_loc', 'block_name', 'source_func','test_prep']
    res_csv = pd.read_csv(res_csv_filename, usecols=columns, header=0, encoding='unicode_escape')
    res_csv.rename(columns={'sink_loc': 'sink', 'source_loc': 'source', 'block_name': 'blocks', 'source_func': 'function'}, inplace=True)
    res_csv['filepath'] = res_csv['sink'].apply(lambda x: dh.getFilepath(x))
# 对每个行进行处理
    for index, row in res_csv.iterrows():
        res_csv.at[index, 'sink'] = dh.parse_location(row['sink'])
        res_csv.at[index, 'source'] = dh.parse_location(row['source'])
        res_csv.at[index, "blocks"] = row["blocks"]
        res_csv.at[index, "function"] = row["function"]
    print(res_csv)
    #res_csv.to_csv("test.csv", index=False, encoding='utf-8')
    tmp_array = np.array(res_csv)
    res_list = tmp_array.tolist()
    #TODO:remove those comments after debug
    #print("[*]Removing ths raw result csv file,bye!")
    #os.remove(res_csv_filename)
    #print(res_list)
    return judge_share(remove_duplicate_list(res_list), source_path)

def result_cleaning_for_wxml(res_csv_filename):
    print("[*]Get the res_file:"+res_csv_filename)
    #TODO:remember to release
    print("Rewriting the res csv file...")
    columns = ['target_element_loc', 'raw_file_path']
    #UPGRADED:test_prep
    #columns = ['sink_loc', 'source_loc', 'block_name', 'source_func','test_prep']
    res_csv = pd.read_csv(res_csv_filename, usecols=columns, header=0, encoding='unicode_escape')
    #res_csv.rename(columns={'sink_loc': 'sink', 'source_loc': 'source', 'block_name': 'blocks', 'source_func': 'function'}, inplace=True)
    #res_csv['filepath'] = res_csv['sink'].apply(lambda x: dh.getFilepath(x))
# 对每个行进行处理
    for index, row in res_csv.iterrows():
        res_csv.at[index, 'target_element_loc'] = dh.parse_location(row['target_element_loc'])
        res_csv.at[index, 'raw_file_path'] = row["raw_file_path"]
    print(res_csv)
    res_csv.to_csv(res_csv_filename, index=False, encoding='utf-8')
    return res_csv_filename
    #tmp_array = np.array(res_csv)
    #res_list = tmp_array.tolist()
    #TODO:remove those comments after debug
    #print("[*]Removing ths raw result csv file,bye!")
    #os.remove(res_csv_filename)
    #print(res_list)



'''
def result_cleaning(res_csv_filename, source_path):
    print("[*]Get the res_file:" + res_csv_filename)
    # TODO:remember to release
    print("Rewriting the res csv file...")
    columns = ['sink_loc', 'source_loc', 'block_name', 'source_func', 'test_prep']
    res_csv = pd.read_csv(res_csv_filename, usecols=columns, header=0, encoding='unicode_escape')
    res_csv.rename(
        columns={'sink_loc': 'sink', 'source_loc': 'source', 'block_name': 'blocks', 'source_func': 'function'},
        inplace=True)
    res_csv['filepath'] = res_csv['sink'].apply(lambda x: dh.getFilepath(x))

    # 对每个行进行处理
    for index, row in res_csv.iterrows():
        res_csv.at[index, 'sink'] = dh.parse_location(row['sink'])
        res_csv.at[index, 'source'] = dh.parse_location(row['source'])
        res_csv.at[index, "blocks"] = row["blocks"]
        res_csv.at[index, "test_prep"] = row["test_prep"]
        res_csv.at[index, "function"] = judge_prep_function(row["function"], row["test_prep"])

    res_csv.drop("test_prep", axis=1, inplace=True)
    print(res_csv)
    # res_csv.to_csv("test.csv", index=False, encoding='utf-8')
    tmp_array = np.array(res_csv)
    res_list = tmp_array.tolist()
    print("[*]Removing the raw result csv file, bye!")
    #TODO:DEBUG ONLY,PLEASE REMOVE THIS IN FINAL VERSION.
    #os.remove(res_csv_filename)
    # print(res_list)
    return judge_share(remove_duplicate_list(res_list), source_path)
'''


def judge_prep_function(function, test_prep):
    # 根据test_prep列的值决定function列的值
    if "functi ..." in test_prep:
        return function
    else:
        return test_prep


def simplify_csv(csv_path):
    print("[*]Removing duplicate source rows...")
    #df = pd.read_csv(csv_path, header=0,index_col=False)
    #df = pd.read_csv(csv_path, header=None, names=['', 'sink', 'source', 'raw_filepath', 'function'], index_col=False)
    with open(csv_path, 'r',encoding='utf-8',) as f:
        header = f.readline().strip()
        df = pd.read_csv(f, header=None, encoding='utf-8',names=['', 'sink', 'source', 'raw_filepath', 'function'])
    #print(df)
    #df['key'] = df['sink'] + '|' + df['source']
    df['length'] = df['source'].apply(len)
    df = df.sort_values(['length'], ascending=[False])
    #df.to_csv("aftersort.csv", index=False, header=0)
    #print(df)
    df = df.drop_duplicates(subset='sink', keep='first')
    df = df[['', 'sink', 'source', 'raw_filepath', 'function']]
    df.columns = ['index', 'sink', 'source', 'raw_filepath', 'function']
    df.to_csv(csv_path, index=False, header=None,encoding='utf-8')
    with open(csv_path, 'r',encoding='utf-8') as f:
        lines = f.readlines()
    lines.insert(0, 'index,sink,source,raw_filepath,function\n')
    with open(csv_path, 'w',encoding='utf-8') as f:
        f.writelines(lines)
    return True


'''def judge_source_function(main_csv, aux_csv, wx_id):
    res_dir = gl.get_value("res_dir")
    res_file_name = res_dir + "/" + wx_id + ".csv"

    main_df = pd.read_csv(main_csv)
    aux_df = pd.read_csv(aux_csv)

    # check if the two dataframes are equal
    if main_df.shape == aux_df.shape:
        if main_df.equals(aux_df):
            # if the dataframes are equal, output main_df as the final csv file
            main_df.to_csv(res_file_name, quoting=csv.QUOTE_ALL, index=False)
        else:
            # find the rows where the source_func column is not equal between main_df and aux_df
            diff_rows = main_df[main_df['source_func'] != aux_df['source_func']]

            # create a copy of main_df to modify for the final output
            output_df = main_df.copy()

            # iterate over the rows where the source_func columns are different
            for index, row in diff_rows.iterrows():
                # check if the row contains the string '(functi' in the source_func column
                if 'functi .' or '.js"' in row['source_func']:
                    # if the row contains the string '(functi' in the source_func column,
                    # replace the source_func value in output_df with the value from aux_df
                    aux_row = aux_df.loc[(aux_df['sink_loc'] == row['sink_loc']) &
                                         (aux_df['source_loc'] == row['source_loc']) &
                                         (aux_df['block_name'] == row['block_name'])]
                    output_df.at[index, 'source_func'] = aux_row.iloc[0]['source_func']

            # output the final dataframe to csv
            output_df.to_csv(res_file_name, index=False,
                             columns=['sink_loc', 'source_loc', 'block_name', 'source_func'],
                            quoting = csv.QUOTE_ALL, quotechar = '"'
                             )
    else:
        output_df = main_df.copy()  # 创建一个output_df用于输出
        # 遍历aux_df
        for i in range(len(aux_df)):
            aux_row = aux_df.iloc[i]  # 取出aux_df的一行
            # 在main_df中查找是否有相同的行，即sink_loc、source_loc和block_name都相同，但是source_func不同
            mask = (main_df['sink_loc'] == aux_row['sink_loc']) & (main_df['source_loc'] == aux_row['source_loc']) & (
                        main_df['block_name'] == aux_row['block_name']) & (
                               main_df['source_func'] != aux_row['source_func'])
            if not main_df[mask].empty:
                # 找到了相同的行，修改output_df中的source_func列
                output_df.loc[mask, 'source_func'] = aux_row['source_func']

        # 输出修改后的output_df
        output_df.to_csv(res_file_name, index=False, columns=['sink_loc', 'source_loc', 'block_name', 'source_func'],
                         quoting=csv.QUOTE_ALL, quotechar='"')

    main_df = pd.read_csv(main_csv)
    aux_df = pd.read_csv(aux_csv)

    # Check if source_func column is identical in both dataframes
    if main_df['source_func'].equals(aux_df['source_func']):
        print("Same source functions.")
        # If yes, main_csv is the final csv file
        main_df.to_csv(res_dir + "/" + wx_id + ".csv", index=False)
    else:
        # If not, create a new dataframe for the final csv file
        print("Replacing source functions...")
        final_df = pd.DataFrame(columns=main_df.columns)
        for i, row in main_df.iterrows():
            #if row['source_func'].startswith('(functi'):
            print(str(row['source_func']))
            if 'functi .' in str(row['source_func']):
                print("Found")
                aux_row = aux_df.loc[aux_df['source_func'] == row['source_func']]
                print("So now changingmaux and main is:",str(aux_df['source_func']),str(row['source_func']))
                if len(aux_row) == 1:
                    final_df = final_df.append(aux_row)
                else:
                    final_df = final_df.append(row)
            else:
                final_df = final_df.append(row)
    
    
     main_df = pd.read_csv(main_csv)
    aux_df = pd.read_csv(aux_csv)

    # 判断main_csv和aux_csv的source_func列是否完全一致
    if set(main_df['source_func']) == set(aux_df['source_func']):
        # 完全一致，输出main_csv为最终csv文件
        main_df.to_csv(wx_id + ".csv", index=False, quoting=csv.QUOTE_ALL, quotechar='"')
    else:
        # 有行不一致，生成新的csv文件
        res_df = pd.DataFrame(columns=['sink_loc', 'source_loc', 'block_name', 'source_func'])
        for _, row in main_df.iterrows():
            if row['source_func'] in aux_df['source_func'].values:
                aux_row = aux_df.loc[aux_df['source_func'] == row['source_func']].iloc[0]
                if 'functi .' in row['source_func']:
                    res_row = aux_row
                else:
                    res_row = row
            else:
                res_row = row
            res_df = res_df.append(res_row, ignore_index=True)
        # Save the final csv file
        res_df.to_csv(res_dir + "/" + wx_id + ".csv", index=False, quoting=csv.QUOTE_ALL, quotechar='"')'''

def judge_source_function(main_csv, aux_csv, wx_id):
    res_dir = gl.get_value("res_dir")
    res_file_name = res_dir + "/" + wx_id + ".csv"

    main_df = pd.read_csv(main_csv)
    aux_df = pd.read_csv(aux_csv)

    output_df = pd.DataFrame(columns=['sink_loc', 'source_loc', 'block_name', 'source_func'])

    for i in range(len(main_df)):
        main_row = main_df.iloc[i]
        aux_row = aux_df[(aux_df['sink_loc'] == main_row['sink_loc']) &
                         (aux_df['source_loc'] == main_row['source_loc']) &
                         (aux_df['block_name'] == main_row['block_name']) &
                         (aux_df['source_func'] != main_row['source_func'])]
        #print("main_row________aux_row.iloc[0]")
        #print(main_row,aux_row.iloc[0])
        #print("___debug only___")
        if not aux_row.empty:
            if 'functi .' in main_row['source_func'] or '.js"' in main_row['source_func']:
                print("main_df source function not function")
            elif 'functi .' in str(aux_row.iloc[0]['source_func']) or '.js"' in str(aux_row.iloc[0]['source_func']):
                # 如果在aux_df该行的['source_func']列中包含'functi .'或'.js"'，则跳过
                print("aux df:source_func may not a function.")
                output_row = {'sink_loc': main_row['sink_loc'],
                              'source_loc': main_row['source_loc'],
                              'block_name': main_row['block_name'],
                              'source_func': main_row['source_func']}
                output_df = output_df.append(output_row, ignore_index=True)
            else:
                # 构建新的一行，取sink_loc，source_loc和block_name为两者相同的值，source_func列则取aux_df对应这行的值，加入output_df中
                output_row = {'sink_loc': main_row['sink_loc'],
                              'source_loc': main_row['source_loc'],
                              'block_name': main_row['block_name'],
                              'source_func': aux_row.iloc[0]['source_func']}
                output_df = output_df.append(output_row, ignore_index=True)

        else:
            # 如果aux_df中没有与main_df中该行匹配的行，将main_df中该行直接加入output_df中
            output_row = {'sink_loc': main_row['sink_loc'],
                          'source_loc': main_row['source_loc'],
                          'block_name': main_row['block_name'],
                          'source_func': main_row['source_func']}
            output_df = output_df.append(output_row, ignore_index=True)

    # 将output_df输出到csv文件中
    output_df.to_csv(res_file_name, index=False,
                     columns=['sink_loc', 'source_loc', 'block_name', 'source_func'],
                     quoting=csv.QUOTE_ALL, quotechar='"')


def check_csv_header_only(file_path):
    with open(file_path, newline='',encoding='unicode_escape') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None) # 获取第一行数据
        if headers is not None and len(headers) > 0 and all(x == '' for x in headers[1:]):
            # 如果第一行不为空且除了第一列外其他列都是空，则只有表头
            return True
    return False