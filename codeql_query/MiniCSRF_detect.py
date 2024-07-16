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


class QueryRunTimeoutError(Exception):
    pass


def miniCSRF_detect(miniapp_dict,query_dir,dec_dir,not_empty,sub_dir):
    WXAPKG_FLAG = 'V1MMWX'
    WXAPKG_FLAG_LEN = len(WXAPKG_FLAG)
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
    try:
        if gl.get_value("platform")=="wechat" and str(sub_dir).startswith("wx",0,2):
            print("[*]Analyzing the WeChat mini-program now..")
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
                    if (gl.get_value("source_platform") == "windows" and "__APP__.wxapkg" in tar) or (gl.get_value("source_platform") == "android" and ".wxapkg" in tar):
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
                            return
                        if not os.path.exists(res_dir+"/potential_obfuscated_applet.txt"):
                            open(res_dir+"/potential_obfuscated_applet.txt", 'w').close()
                        with open(res_dir+"/potential_obfuscated_applet.txt", mode="r") as file_2:
                            existing_appids_2 = file_2.read().splitlines()
                        if appid in existing_appids_2:
                            print(f"[!]appid {appid} already analyzed. Skipping.")
                            return
                        obfuscated_file_path = res_dir + "/analyzed_applet.txt"
                        #over
                        print("[*]Appid:",gl.get_value("appid"))
                        source_path = dec_dir+"/"+appid+"_dec"
                        gl.set_value("source_path",source_path)
                        #res_source_path = "/data/disk_16t_2/zidong/applet_query/res/"+appid+"_final.csv"
                        #if os.path.exists(res_source_path):
                        #    print("[*]detected before.")
                        #    continue
                        try:
                            if gl.get_value("source_platform") == "android":
                                print("[*]Maybe decrypted.")
                                new_filename = os.path.join(dec_dir, appid + "_dec.wxapkg")
                                shutil.copy(tar, new_filename)
                            else:
                                print("[*]decrypting...")
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
                                os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                                op.analyzed_summary(appid)
                                op.decrypted_failed(appid)
                                print("unpacking failed lol.")
                                return True
                            os.chdir(now_pwd)
                        except Exception as e:
                            traceback.print_exc()
                            #os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                            print("decryption failed lol.")
                            os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                            op.analyzed_summary(appid)
                            op.decrypted_failed(appid)
                            return True
                        #global source_path_list
                        #source_path_list.append("E:/weapp/codeql_test/dec_dir/"+sub_dir+"_dec")
                        dec_path = dec_dir+"/"+appid+"_dec.wxapkg"
                        if os.path.exists(dec_path):
                            os.remove(dec_path)
                        else:
                            #os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                            print("decryption failed.")
                            op.analyzed_summary(appid)
                            op.decrypted_failed(appid)
                            return True
                        if gl.get_value("decrypted_only_flag")=="yes":
                            print("[*]Decrypted Over.Ty for your usage .")
                            exit(0)
                        wxml_query_dbname = Mimikyu.wxml_to_html_convert(source_path,appid)
                        session_check_res = Mimikyu.query_wechat_reborn(source_path,appid,wxml_query_dbname) #source code query
                        #TODO:remember to release this.
                        final_res = rh.result_cleaning(query_dir+"/res/"+appid+".csv",source_path) #wxid_final.csv
                        #gl.set_value("res_dir",query_dir+"/res")
                        #session_check_res = Mimikyu.query_session(source_path,appid) #return:the _SessionCheck.csv filepath
                        op.convert_to_csv(final_res, appid, wxml_query_dbname) #seem Correct
                        final_X_csv = op.session_check(query_dir+"/res/"+appid+"_final_new.csv",session_check_res)
                        #appid, nickname, cate, domain_list=hh.get_domain_info()
                        appid = gl.get_value("appid")
                        op.collect_csv_finally(final_X_csv,appid) #need to fix bugs:useless loop for appid
                        hh.get_domain_info(appid)
                        #op.write_final_list_X(appid, nickname, cate, domain_list)
                        op.remove_redundant(appid)
                        #op.remove_dec_dir(dec_dir+"/"+appid+"_dec")
                        end_time = time.time()
                        run_time = end_time - start_time
                        print("[*]Static analysis done.Please check /res directory.")
                        print("Run time of this round:",run_time)
                        op.time_to_csv(appid,run_time)
                        op.analyzed_summary(appid)
                        os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                        #os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
        elif gl.get_value("platform")=="baidu" and str(sub_dir):
            print("[*]Analyzing the Baidu mini-program now..")
            start_time = time.time()
            not_empty = True
            print(sub_dir)
            appid = sub_dir
            #gl.set_value("appid",appid)
            #appid_list.append(sub_dir)
            print(miniapp_dict+"/"+appid)
            g = os.walk(miniapp_dict+"/"+appid)
            for path,dir_list,file_list in g:
                print("hi")
                for file_name in file_list:
                    print("path:",path)
                    tar = os.path.join(path, file_name)
                    print("tar:",tar)
                    print("Now checking the applet's dir...:",tar)
                    #gl.set_value("appid", appid)
                    if "app.js" in tar:
                        gl.set_value("appid", appid)
                        #judging if applet has been analyzed.
                        res_dir = gl.get_value("res_dir")
                        analyzed_file_path = res_dir + "/analyzed_applet_baidu.txt"
                        if not os.path.exists( analyzed_file_path):
                            open( analyzed_file_path, 'w').close()
                        with open(analyzed_file_path, mode="r") as file:
                            existing_appids = file.read().splitlines()
                        if appid in existing_appids:
                            print(f"[!]appid {appid} already analyzed. Skipping.")
                            return
                        if not os.path.exists(res_dir+"/potential_obfuscated_applet_baidu.txt"):
                            open(res_dir+"/potential_obfuscated_applet_baidu.txt", 'w').close()
                        with open(res_dir+"/potential_obfuscated_applet_baidu.txt", mode="r") as file_2:
                            existing_appids_2 = file_2.read().splitlines()
                        if appid in existing_appids_2:
                            print(f"[!]appid {appid} already analyzed. Skipping.")
                            return
                        #over
                        #res_source_path = "/data/disk_16t_2/zidong/applet_query/res/"+appid+"_final.csv"
                        #if os.path.exists(res_source_path):
                        #    print("[*]detected before.")
                        #    continue
                        try:
                            #p = subprocess.Popen(['python', query_dir+'/wechat_miniapp_dec.py', '--wxid', appid,'--file',tar,'-o',dec_dir+"/"+appid+"_dec.wxapkg"], stdin = subprocess.PIPE, stdout=subprocess.PIPE)
                            #handling the baidu smapp unpacker
                            now_pwd = os.getcwd()
                            os.chdir(query_dir+"/baidu_smapp_unpacker") #for Linux only
                            #run unpack script by distinguishing the system platform
                            # intall the dependency
                            if not os.path.exists("node_modules"):
                                # 如果没有，执行npm install
                                process = subprocess.Popen(["npm", "install"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                stdout, stderr = process.communicate()
                                if process.returncode != 0:
                                    print(f"Error occurred: {stderr.decode('utf-8')}")
                                else:
                                    print(f"Success: {stdout.decode('utf-8')}")
                            else:
                                print("[*]Unpacking the baidu smapp...")
                                command = ["node", "baiduUnpacker.js", appid]
                                # 使用subprocess.Popen执行命令
                                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                # 等待命令执行完成
                                stdout, stderr = process.communicate()
                                # 打印输出和错误信息（如果有的话）
                                if process.returncode != 0:
                                    print(f"Error occurred: {stderr.decode('utf-8')}")
                                else:
                                    print(f"Success: {stdout.decode('utf-8')}")
                            print("[*]Appid:",gl.get_value("appid"))
                            source_path = dec_dir+"/"+appid+"_dec"
                            gl.set_value("source_path",source_path)
                            # try:
                            #     if platform.system() == "Linux":
                            #         q = subprocess.Popen(
                            #             [query_dir+"/wxappUnpacker/bingo.sh",dec_dir+"/"+appid+"_dec.wxapkg"],
                            #             stdin = subprocess.PIPE, stdout=subprocess.PIPE)
                            #     elif platform.system() == "Windows":
                            #         q = subprocess.Popen(
                            #             [query_dir+"/wxappUnpacker/bingo.bat",dec_dir+"/"+appid+"_dec.wxapkg"],
                            #             stdin = subprocess.PIPE, stdout=subprocess.PIPE)
                            #     out_q = q.stdout.readlines()
                            #     print(out_q)
                            # except:
                            #     os.chdir(now_pwd)
                            #     os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                            #     op.analyzed_summary(appid)
                            #     op.decrypted_failed(appid)
                            #     print("unpacking failed lol.")
                            #     return True
                            # os.chdir(now_pwd)
                        except:
                            #os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                            print("decryption failed lol.")
                            os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                            op.analyzed_summary(appid)
                            op.decrypted_failed(appid)
                            return True
                        #global source_path_list
                        #source_path_list.append("E:/weapp/codeql_test/dec_dir/"+sub_dir+"_dec")
                        # dec_path = dec_dir+"/"+appid+"_dec.wxapkg"
                        # if os.path.exists(dec_path):
                        #     os.remove(dec_path)
                        # else:
                        #     #os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                        #     print("decryption failed.")
                        #     op.analyzed_summary(appid)
                        #     op.decrypted_failed(appid)
                        #     return True
                        #wxml_query_dbname = Mimikyu.wxml_to_html_convert(source_path,appid)
                        swan_query_dbname = Mimikyu.swan_to_html_convert(source_path,appid)
                        #session_check_res = Mimikyu.query_wechat_reborn(source_path,appid,wxml_query_dbname) #source code query
                        baidu_session_check_res = Mimikyu.query_baidu_reborn(source_path,appid,swan_query_dbname)
                        #TODO:remember to release this.
                        final_res = rh.result_cleaning(query_dir+"/res/"+appid+".csv",source_path) #wxid_final.csv
                        #gl.set_value("res_dir",query_dir+"/res")
                        #session_check_res = Mimikyu.query_session(source_path,appid) #return:the _SessionCheck.csv filepath
                        op.convert_to_csv_baidu(final_res, appid, swan_query_dbname) #seem Correct
                        final_X_csv = op.session_check(query_dir+"/res/"+appid+"_final_new.csv",baidu_session_check_res)
                        #appid, nickname, cate, domain_list=hh.get_domain_info()
                        appid = gl.get_value("appid")
                        op.collect_csv_finally_baidu(final_X_csv,appid) #need to fix bugs:useless loop for appid
                        #hh.get_domain_info(appid)
                        #op.write_final_list_X(appid, nickname, cate, domain_list)
                        op.remove_redundant(appid)
                        #op.remove_dec_dir(dec_dir+"/"+appid+"_dec")
                        end_time = time.time()
                        run_time = end_time - start_time
                        print("[*]Static analysis done.Please check /res directory.")
                        print("Run time of this round:",run_time)
                        op.time_to_csv(appid,run_time)
                        op.analyzed_summary(appid)
                        os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
                        #os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
        
        elif not_empty is None:
            print("[!]No applet in your miniapp_dict,Please check your config file.")
            exit(1)

    except subprocess.TimeoutExpired:
        op.analyzed_summary(appid)
        os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
        #op.potential_obfuscation(appid)
        traceback.print_exc()
        print("Query execution timed out")
        return True
    except Exception as e:
        print("_____exception_____")
        op.analyzed_summary(appid)
        os.rename(miniapp_dict + "/" + appid, miniapp_dict + "/analyzed_" + appid)
        traceback.print_exc()
        print("Noting happended,keep going")
        return True
    return True
