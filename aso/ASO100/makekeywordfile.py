# -*- coding: utf-8 -*-
import re
import time
import datetime
import traceback
from string import zfill
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import MySQLdb
import xlsxwriter
import xlwt
import xlrd
import os


def readFile(path,filename,dataList):
    query_date = re.compile(r'_(\d+)').findall(filename)[0]
    query_time = query_date[:4]+"-"+query_date[4:6]+"-"+query_date[6:]
    data = xlrd.open_workbook(path)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    for i in range(nrows):
        keywordRank = []
        # for j in range(2):
        # a = table.row_values(i)
        keywordRank.append(table.row(i)[0].value)
        keywordRank.append(table.row(i)[1].value)
        keywordRank.append(query_time)
        dataList.append(keywordRank)
    return dataList

def GetFileList(dir, fileList):
    if os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            if s == ".DS" or s == ".DS_Store":
                continue
            fileList.append(s)
    return fileList

def makeFile(path_des,filename,appName,result):
    #携程旅行_关键词覆盖数据_20161102.xlsx
    w = xlsxwriter.Workbook(path_des+filename)
    ws = w.add_worksheet('ASO100')
    ws.write(0,0,appName)
    ws.write(0,1, u'关键词')
    ws.write(0,2, u'排名')
    ws.write(0,3, u'日期')
    for i in range(0, len(result)):
        for j in range(1,len(result[i])):
            # print result[i][j]
            ws.write(i,0,appName)
            ws.write(i, 1, result[i][j][0])
            ws.write(i, 2, result[i][j][1])
            ws.write(i, 3, result[i][j][2])
    w.close()


def start():

    srcPath = "/Users/Zyang/Documents/ASO/ASO_keyword/11.five/"
    dirList = GetFileList(srcPath, [])


    for appIndex in range(0,len(dirList)):
        try:
            appName = str(dirList[appIndex])
            result = []

            try:
                w = xlsxwriter.Workbook("/Users/Zyang/Documents/ASO/ASO_keyword/11.ok/" +appName+"/"+appName+"_keywordyear.xlsx")
                # w = xlsxwriter.Workbook("/Users/Zyang/Documents/ASO/oneyearkeyword/"+appName+"_keyWord.xlsx")
            except:
                traceback.print_exc()
                continue

            ws = w.add_worksheet('ASO100')

            ws.write(0, 0, "appName")
            ws.write(0, 1, u'关键词')
            ws.write(0, 2, u'排名')
            ws.write(0, 3, u'日期')
            row = 1

            for xlFile in os.listdir(srcPath + appName):

                if xlFile == ".DS" or xlFile == ".DS_Store":
                    continue
                list = readFile(srcPath + appName + "/" + xlFile, xlFile, [])
                # print list[1][1]
                # result.append(list)

                for i in range(1, len(list)):

                    try:
                        # print result[i][j]
                        ws.write(row, 0, str(appName))
                        ws.write(row, 1, list[i][0])
                        ws.write(row, 2, list[i][1])
                        ws.write(row, 3, list[i][2])
                        row += 1
                    except:
                        traceback.print_exc()
            w.close()
            print "app+1"+appName
        except:
            traceback.print_exc()
            print "没目录!!!!!"+appName
            continue

start()
# makeFile("/Users/Zyang/Documents/ASO/123/","keyword.xlsx")
# list = readFile("/Users/Zyang/Documents/ASO2/蚂蜂窝自由行/蚂蜂窝自由行_关键词覆盖数据_20161103.xlsx",[])
# print list
# for i in range(1,len(list)):
#     print list[i]