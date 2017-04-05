# coding:utf-8
import os
from shutil import copyfile, copytree, move

import xlrd


def GetFileList(dir, fileList):
    if os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            if s == ".DS" or s == ".DS_Store":
                continue
            fileList.append(s)
    return fileList
path = "/Users/Zyang/Dropbox/ASO数据/旅游分类数据/ASO_FILE_待补充数据/"
# path = "/Users/Zyang/Dropbox/ASO数据/旅游分类数据/ASO_FILE/"
# path = "/Users/Zyang/Documents/ASO/ASO_FILE/travel/"
list = GetFileList(path,[])

for i in list:

    xlsxList = []
    for s in os.listdir(path+i+"/"):
        if s == ".DS" or s == ".DS_Store":
            continue
        xlsxList.append(s)
    # print len(xlsxList)
    if len(xlsxList)==4:
        # move(path+i,"/Users/Zyang/Dropbox/ASO数据/旅游分类数据/ASO_FILE/"+i+"/")
        move(path + i, "/Users/Zyang/Dropbox/ASO数据/旅游分类数据/ASO_FILE/" + i + "/")
