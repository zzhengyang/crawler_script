# coding=utf-8
'''
Created on 2016-10-24

@author: zy
'''
import os
import re
import shutil

import time


def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            # if s == "xxx":
            # continue
            newDir = os.path.join(dir, s)
            GetFileList(newDir, fileList)
    return fileList


lists = GetFileList('/Users/Zyang/Downloads/keyword', [])
list = []

for e in lists:
    filename = re.findall(r'keyword/(.*?)_', str(e))
    if filename:
        if filename[0] not in list:
            list.append(filename[0])
    else:
        continue


def mkdir(list):


    for i in list:
        path = "/Users/Zyang/Documents/ASO/ASO_keyword/11.five/" + str(i)
        try:
            os.makedirs(path)
        except OSError, e:
            continue

def mvfile(lists):
    for i in lists:
        path_src = str(i)
        file_name = path_src.replace('/Users/Zyang/Downloads/keyword/', '')
        filename = re.findall(r'keyword/(.*?)_', str(i))
        if filename:
            path_des = "/Users/Zyang/Documents/ASO/ASO_keyword/11.five/" + str(filename[0])  # + "/"+ str(file_name)
            print path_src + "====" + path_des + "=====" + file_name
            try:
                shutil.move(path_src, path_des)
            except:
                continue
        else:
            continue

mkdir(list)
time.sleep(3)
mvfile(lists)