#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA1
from Cryptodome.Cipher import AES

# 微信小程序包 自定义标识
WXAPKG_FLAG = 'V1MMWX'
WXAPKG_FLAG_LEN = len(WXAPKG_FLAG)

def main():

    parser = argparse.ArgumentParser(description='PC WeChat miniapp wxapkg package decryption tool')
    parser.add_argument('--wxid', metavar='WeChat applet ID', required=True)
    parser.add_argument('--iv', metavar='iv', required=False, default='the iv: 16 bytes')
    parser.add_argument('--salt', metavar='salt', required=False, default='saltiest')
    parser.add_argument('-f', '--file', metavar='Encrypted miniapp file path', required=True)
    parser.add_argument('-o', '--output', metavar='Decrypted miniapp file path', required=True)

    args = parser.parse_args()

    key = PBKDF2(args.wxid.encode('utf-8'), args.salt.encode('utf-8'), 32, count=1000, hmac_hash_module=SHA1)

    # 读取加密的内容
    if not os.path.exists(args.file):
        raise Exception('file does not exist')

    with open(args.file, mode='rb') as f:
        dataByte = f.read()

    if dataByte[0:WXAPKG_FLAG_LEN].decode() != WXAPKG_FLAG:
        raise Exception('This file does not need to be decrypted, or it is not a WeChat applet wxapkg encrypted package')

    # 初始化密钥
    cipher = AES.new(key, AES.MODE_CBC, args.iv.encode('utf-8'))
    
    # 解密头部1024个字节
    originData = cipher.decrypt(dataByte[WXAPKG_FLAG_LEN: 1024 + WXAPKG_FLAG_LEN])

    # 初始化xor密钥, 解密剩余字节
    xorKey = 0x66
    if len(args.wxid) >= 2:
        xorKey = ord(args.wxid[len(args.wxid) - 2])

    afData = dataByte[1024 + WXAPKG_FLAG_LEN:]

    out = bytearray()
    for i in range(len(afData)):
        out.append(afData[i] ^ xorKey)

    originData = originData[0:1023] + out

    # 保存解密后的数据
    with open(args.output, mode='wb') as f:
        f.write(originData)

    print('Decrypted successfully.', args.output)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        print("decrypted failed.")
