import pandas as pd
import numpy as np
import utility.dataHandler as dh
import utility.globalvar as gl
import utility.output as op
import re
import os
import subprocess
import csv
import shutil
import requests


# def get_domain_info():
#     print("[*]Getting the domain information of applets...")
#     # open the file
#     res_dir = gl.get_value("res_dir")
#     if os.path.exists(res_dir+"/final_res.csv"):
#         raw_res_query = pd.read_csv(res_dir+"/final_res.csv", encoding='unicode_escape')
#         print(raw_res_query)
#         appid_list = np.array(raw_res_query["wechat_app_id"]).tolist()
#         print(appid_list)
#     else:
#         print("[*]Not found final_res.csv,what's wrong?")
#         return True
#     '''
#     # 输出所有文件和文件夹
#     for file in dirs:
#         if str(file).startswith("wx",0,2):
#             print(file)
#             appid_list.append(file)
#     '''
#     #print(appid_list)

#     headers = {'Host': 'mp.weixin.qq.com',
#                'Connection': 'keep-alive',
#                'X-WECHAT-KEY': "81c3e4708616e1830dd7d5cc41d602a31827b409a40b7b55242bee9e35c691f1b58047d1e571795bd5d59a5a00085420ad3120ef6cd72eb616edb3f4881cc9cd0adbedb20c9606225fe0fffcaae7d82bfc21b6524c4b135f9985309d970d7e097c12dfe2b16375ba04ade5a697b93c8f9130e07511091bf11e0f7fb042a9708b",
#                'X-WECHAT-UIN': 'MTM2MjQ0MjY4Nw%3D%3D',
#                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000733) NetType/WIFI Language/zh_CN',
#                'Accept-Encoding': 'gzip, deflate, br',
#                }
#     for appid in appid_list:
#         # get metadatas of miniapp
#         detail_url = 'https://mp.weixin.qq.com/wxawap/waverifyinfo?action=get&appid=%s' % str(appid)
#         # detail_url = 'https://mp.weixin.qq.com/wxawap/waverifyinfo?action=get&appid=wx05accd64f94c3988'
#         detail = requests.get(detail_url, headers=headers)
#         # print(detail.text)
#         resp = detail.text.replace(' ', '').replace('\n', '').replace('\t', '').replace("\"", "")
#         # get request_domain information
#         #print(resp)
#         # if "category_list:{:[" in resp:
#         #    print("find the category.")
#         if "request_domain:{item:[" in resp:
#             print("[*]Found the domain list.")
#             domain_list = dh.Get_MiddleStr(resp, "request_domain:{item:[", ",]}};</sc")
#             # print(domain_list)
#             # for d in final_domain_list:
#             #    final_domain_list.append(d)
#             # domain_list.insert(0,'------')
#             # domain_list.insert(0,appid)
#             print(appid, domain_list)

#             # final_domain_list2.append(domain_list)
#             # print(final_domain_list2)
#             # write_domain_list(appid, domain_list, final_domain_list2)
#             # write_domain_list(appid, domain_list)

#         # get nickname
#         if "nickname:" in resp:
#             nickname = dh.Get_MiddleStr_only(resp, "nickname:", ",wxaproduct_qua_size")
#             print("[*]Found nickname:",nickname)

#         if "category_list:{cate:[" in resp:
#             #print("!!!")
#             # endstr:]},
#             cate = dh.Get_MiddleStr_only(resp, "category_list:{cate:[", "]},desc")
#             print("[*]Found category name:",cate)
#         '''
#         if os.path.exists(res_dir+"/final_res.csv"):
#             # raw_res = pd.read_csv("E:\weapp\codeql_test\res\final_res.csv",encoding= 'unicode_escape')
#             rawres_path = "/data/disk_16t_2/zidong/applet_query/res/final_res.csv"
#         else:
#             print("Reuslt not found.")
#         '''
#         print("____appid, nickname, cate, domain_list____")
#         print(appid, nickname, cate, domain_list)
#         print("______")
#         op.write_final_list(appid, nickname, cate, domain_list)
#         op.write_final_list_X(appid, nickname, cate, domain_list)
#         #return appid, nickname, cate, domain_list
#         # return appid,nickname,cate,domain_list

def get_domain_info(appid):
    # print("[*]Getting the domain information of applets...")
    # # open the file
    # res_dir = gl.get_value("res_dir")
    # if os.path.exists(res_dir+"/final_res.csv"):
    #     raw_res_query = pd.read_csv(res_dir+"/final_res.csv", encoding='unicode_escape')
    #     print(raw_res_query)
    #     appid_list = np.array(raw_res_query["wechat_app_id"]).tolist()
    #     print(appid_list)
    # else:
    #     print("[*]Not found final_res.csv,what's wrong?")
    #     return True
    # '''
    # # 输出所有文件和文件夹
    # for file in dirs:
    #     if str(file).startswith("wx",0,2):
    #         print(file)
    #         appid_list.append(file)
    # '''
    # #print(appid_list)

    headers = {'Host': 'mp.weixin.qq.com',
               'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000733) NetType/WIFI Language/zh_CN',
               'Cookie': 'pass_ticket=PCinnjgwUSoRc74oDaM3vp8yC0PiE7igKN9l6bCvz2VpPPyvRPtZMBgv6xePbtuhPogs2FwGejZnIYSU+2RDEw==; wap_sid2=COr/xgUSdnlfSEdkbmdNek53RzFjbWtqVEZneFZGX3d3SURWbjJJMU1ZWk5xdFNkOEdCNlJqZm90aFJtSF9KaUxzX0g3UEZxQmZXYXBGeTd2dlc4c21pWlJLNG9GQS11UDdMSF9SeUVzcmVyUkdLQzRBaVRoeEJJQUFBfn4wnK3xrQY4DECUTg==; wxuin=06842048851112',
               }
    #for appid in appid_list:
    # get metadatas of miniapp
    detail_url = 'https://mp.weixin.qq.com/wxawap/waverifyinfo?action=get&appid=%s' % str(appid)
    # detail_url = 'https://mp.weixin.qq.com/wxawap/waverifyinfo?action=get&appid=wx05accd64f94c3988'
    detail = requests.get(detail_url, headers=headers)
    # print(detail.text)
    resp = detail.text.replace(' ', '').replace('\n', '').replace('\t', '').replace("\"", "")
    # get request_domain information
    print(resp)
    # if "category_list:{:[" in resp:
    #    print("find the category.")
    if "request_domain:{item:[" in resp:
        print("[*]Found the domain list.")
        #domain_list = dh.Get_MiddleStr(resp, "request_domain:{item:[", ",]}};</sc")

        #updated:2024.02.02
        domain_list = dh.Get_MiddleStr(resp, "request_domain:{item:[", "]},wxa_")
        # print(domain_list)
        # for d in final_domain_list:
        #    final_domain_list.append(d)
        # domain_list.insert(0,'------')
        # domain_list.insert(0,appid)
        print(appid, domain_list)
    else:
        domain_list = []
        # final_domain_list2.append(domain_list)
        # print(final_domain_list2)
        # write_domain_list(appid, domain_list, final_domain_list2)
        # write_domain_list(appid, domain_list)

    # get nickname
    if "nickname:" in resp:
        nickname = dh.Get_MiddleStr_only(resp, "nickname:", ",wxaproduct_qua_size")
        print("[*]Found nickname:",nickname)

    if "category_list:{cate:[" in resp:
        #print("!!!")
        # endstr:]},
        cate = dh.Get_MiddleStr_only(resp, "category_list:{cate:[", "]},desc")
        print("[*]Found category name:",cate)
    '''
    if os.path.exists(res_dir+"/final_res.csv"):
        # raw_res = pd.read_csv("E:\weapp\codeql_test\res\final_res.csv",encoding= 'unicode_escape')
        rawres_path = "/data/disk_16t_2/zidong/applet_query/res/final_res.csv"
    else:
        print("Reuslt not found.")
    '''
    print("____appid, nickname, cate, domain_list____")
    print(appid, nickname, cate, domain_list)
    print("______")
    op.write_final_list(appid, nickname, cate, domain_list)
    op.write_final_list_X(appid, nickname, cate, domain_list)
    #return appid, nickname, cate, domain_list
    # return appid,nickname,cate,domain_list