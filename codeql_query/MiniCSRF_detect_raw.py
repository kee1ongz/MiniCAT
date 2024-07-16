# -*- coding:utf-8 -*-
import platform
import utility.globalvar as gl
import codeql_query.MiniCSRF_query as Mimikyu
import utility.resHandler as rh
import utility.output as op
import utility.httpHandler as hh
import pandas as pd
import numpy as np
import re
import os
import subprocess
import csv
import shutil
import requests
import time
import traceback


def miniCSRF_detect():
    miniapp_dict = gl.get_value("miniapp_dict")
    query_dir = gl.get_value("query_dir")
    #ide_cli = gl.get_value("ide_cli")
    dirs = os.listdir(miniapp_dict)
    if dirs is None:
        print("Nothing in your miniapp_dict,Please check your config file.")
        exit(1)
    print(dirs)
    if not os.path.exists(query_dir+"/dec_dir"):
        print("[*]Crating dec_dir:save decrypted applets.")
        os.mkdir(query_dir+"/dec_dir")
    #gl.set_value("dec_dir",query_dir+"/dec_dir")
    dec_dir = gl.get_value("dec_dir")
    gl.set_value("res_dir",query_dir+"/res")
    #appid_list = []
    not_empty = False
    for sub_dir in dirs:
        try:
            if str(sub_dir).startswith("wx",0,2):
                start_time = time.time()
                not_empty = True
                print(sub_dir)
                appid = sub_dir
                #gl.set_value("appid",appid)
                #appid_list.append(sub_dir)
                g = os.walk(miniapp_dict+"/"+appid)
                for path,dir_list,file_list in g:
                    for file_name in file_list:
                        #print("path:",path)
                        tar = os.path.join(path, file_name)
                        #print("tar:",tar)
                        print("Now checking the applet's dir...:",tar)
                        #gl.set_value("appid", appid)
                        if "__APP__.wxapkg" in tar:
                            gl.set_value("appid", appid)
                            #judging if applet has been analyzed.
                            res_dir = gl.get_value("res_dir")
                            analyzed_file_path = res_dir + "/analyzed_applet.txt"
                            if not os.path.exists( analyzed_file_path):
                                open( analyzed_file_path, 'w').close()
                            with open(analyzed_file_path, mode="r") as file:
                                existing_appids = file.read().splitlines()
                            if appid in existing_appids:
                                print(f"[!]appid {appid} already analyzed. Skipping.")
                                continue
                            #over
                            print("[*]Appid:",gl.get_value("appid"))
                            source_path = dec_dir+"/"+appid+"_dec"
                            gl.set_value("source_path",source_path)
                            #res_source_path = "/data/disk_16t_2/zidong/applet_query/res/"+appid+"_final.csv"
                            #if os.path.exists(res_source_path):
                            #    print("[*]detected before.")
                            #    continue
                            try:
                                p = subprocess.Popen(['python', query_dir+'/wechat_miniapp_dec.py', '--wxid', appid,'--file',tar,'-o',dec_dir+"/"+appid+"_dec.wxapkg"], stdin = subprocess.PIPE, stdout=subprocess.PIPE)
                                out_p = p.stdout.readlines()
                                print(out_p)
                                op.decrypted_summary(appid)
                                now_pwd = os.getcwd()
                                os.chdir(query_dir+"/wxappUnpacker") #for Linux only
                                #run unpack script by distinguishing the system platform
                                try:
                                    if platform.system() == "Linux":
                                        q = subprocess.Popen(
                                            [query_dir+"/wxappUnpacker/bingo.sh",dec_dir+"/"+appid+"_dec.wxapkg"],
                                            stdin = subprocess.PIPE, stdout=subprocess.PIPE)
                                    elif platform.system() == "Windows":
                                        q = subprocess.Popen(
                                            [query_dir+"/wxappUnpacker/bingo.bat",dec_dir+"/"+appid+"_dec.wxapkg"],
                                            stdin = subprocess.PIPE, stdout=subprocess.PIPE)
                                    out_q = q.stdout.readlines()
                                    print(out_q)
                                except:
                                    os.chdir(now_pwd)
                                    print("unpacking failed lol.")
                                    continue
                                os.chdir(now_pwd)
                            except:
                                #os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                                print("decryption failed lol.")
                                continue
                            '''try:
                                p = subprocess.Popen(['python', query_dir+'/wechat_miniapp_dec.py', '--wxid', appid,'--file',tar,'-o',dec_dir+"/"+appid+"_dec.wxapkg"], stdin = subprocess.PIPE, stdout=subprocess.PIPE)
                                out_p = p.stdout.readlines()
                                print(out_p)
                            except:
                                #os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                                print("decryption failed lol.")
                                continue
                            op.decrypted_summary(appid)
                            now_pwd = os.getcwd()
                            os.chdir(query_dir+"/wxappUnpacker") #for Linux only
                            #run unpack script by distinguishing the system platform
                            try:
                                if platform.system() == "Linux":
                                    q = subprocess.Popen(
                                        [query_dir+"/wxappUnpacker/bingo.sh",dec_dir+"/"+appid+"_dec.wxapkg"],
                                        stdin = subprocess.PIPE, stdout=subprocess.PIPE)
                                elif platform.system() == "Windows":
                                    q = subprocess.Popen(
                                        [query_dir+"/wxappUnpacker/bingo.bat",dec_dir+"/"+appid+"_dec.wxapkg"],
                                        stdin = subprocess.PIPE, stdout=subprocess.PIPE)
                                out_q = q.stdout.readlines()
                                print(out_q)
                            except:
                                os.chdir(now_pwd)
                                continue
                            os.chdir(now_pwd)'''
                            #global source_path_list
                            #source_path_list.append("E:/weapp/codeql_test/dec_dir/"+sub_dir+"_dec")
                            dec_path = dec_dir+"/"+appid+"_dec.wxapkg"
                            if os.path.exists(dec_path):
                                os.remove(dec_path)
                            else:
                                #os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                                print("decryption failed.")
                                continue
                            Mimikyu.query_wechat(source_path,appid) #source code query
                            #TODO:remember to release this.
                            final_res = rh.result_cleaning(query_dir+"/res/"+appid+".csv",source_path) #wxid_final.csv
                            #gl.set_value("res_dir",query_dir+"/res")
                            wxml_query_dbname=Mimikyu.wxml_query_prepare(source_path,appid)
                            session_check_res = Mimikyu.query_session(source_path,appid) #return:the _SessionCheck.csv filepath
                            op.convert_to_csv(final_res, appid, wxml_query_dbname)
                            final_X_csv = op.session_check(query_dir+"/res/"+appid+"_final_new.csv",session_check_res)
                            #appid, nickname, cate, domain_list=hh.get_domain_info()
                            appid = gl.get_value("appid")
                            op.collect_csv_finally(final_X_csv,appid)
                            hh.get_domain_info()
                            #op.write_final_list_X(appid, nickname, cate, domain_list)
                            op.remove_redundant(appid)
                            #op.remove_dec_dir(dec_dir+"/"+appid+"_dec")
                            end_time = time.time()
                            run_time = end_time - start_time
                            print("[*]Static analysis done.Please check /res directory.")
                            print("Run time of this round:",run_time)
                            op.time_to_csv(appid,run_time)
                            op.analyzed_summary(appid)
                            #os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                            #os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                            '''
                            os.rename(miniapp_dict+"/"+appid,miniapp_dict+"/analyzed_"+appid)
                            #os.chdir("E:/weapp/codeql_test/res")
                            res_csv_filename ="/data/disk_16t_2/zidong/applet_query/res/"+appid+".csv"
                            print("[*]Get the res_file:"+res_csv_filename)
                            res_csv = pd.read_csv(res_csv_filename,header=0, encoding='unicode_escape')
                            os.remove(res_csv_filename)
                            print(res_csv)
                            for index,row in res_csv.iterrows():
                                row['sink'] = parse_location(row['sink_loc'])
                                row['source'] = parse_location(row['source_loc'])
                                row["blocks"] = row["block_name"]
                                row["function"] = row["source_func"]
                            print(res_csv)
                            tmp_array = np.array(res_csv)
                            res_list = tmp_array.tolist()
                            print(res_list)
                            #print(res_list)
                            #s_path = "E:/weapp/oklok1023/_1027500618_45/"
                            final_res =judge_share(remove_duplicate_list(res_list),source_path)
                            #final2_res=judge_share(final_res,"E:/weapp/oklok1023/_1027500618_45/")
                            convert_to_csv(final_res,appid)
                            get_domain_info()
                            #print("[*]removing this applet,bye...")
                            #shutil.rmtree(sub_dir)
                            print("[*]Done.")
            '''
            elif not_empty is None:
                print("[!]No applet in your miniapp_dict,Please check your config file.")
                exit(1)
        except Exception as e:
            print("_____exception_____")
            op.analyzed_summary(appid)
            traceback.print_exc()
            print("Noting happended,keep going")
            continue
    return True
