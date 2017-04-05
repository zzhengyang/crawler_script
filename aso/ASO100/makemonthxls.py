# coding:utf-8
import os
import re

import MySQLdb
import datetime
import xlrd
import xlsxwriter
import xlwt


def readFile(path,dataList):

    data = xlrd.open_workbook(path)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    for i in range(nrows):
        a = table.row_values(i)

        if not a[0]:
            continue
        dataList.append(a)
    return dataList

def GetFileList(dir, fileList):
    if os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            if s == ".DS" or s == ".DS_Store":
                continue
            fileList.append(s)
    return fileList

def makeFile(path_des,filename,result):
    #携程旅行_关键词覆盖数据_20161102.xlsx
    fileDate = re.compile(r'_(\d+)').findall(filename)[0]
    year = fileDate[0:4]
    month = fileDate[4:6].zfill(2)
    day = fileDate[6:8].zfill(2)
    sdate = year+"-"+month+"-"+day
    tdate = datetime.datetime.strptime(sdate,'%Y-%m-%d')
    makefilename = tdate-datetime.timedelta(days=7)
    smakefilename = makefilename.strftime("%Y-%m-%d")
    newFileName = filename.replace(fileDate,smakefilename).replace("-","")
    w = xlsxwriter.Workbook(path_des + newFileName)
    ws = w.add_worksheet('ASO100')
    ws.write(0, 0, u'关键词')
    ws.write(0, 1, u'排名')
    for i in range(1, len(result)):
        ws.write(i, 0, result[i][0])
        ws.write(i, 1, result[i][1])
    w.close()


def start():

    srcPath = "/Users/Zyang/Documents/ASO/ASO_keyword/11.five/"
    dirList = GetFileList(srcPath,[])
    for appName in dirList:
        for xlFile in os.listdir(srcPath + appName):
            if xlFile == ".DS" or xlFile == ".DS_Store":
                continue

            print xlFile

            query_date = re.compile(r'_(\d+)').findall(xlFile)[0]
            list = readFile(srcPath + appName + "/" + xlFile, [])
            rankList = []
            for i in range(1, len(list)):
                Infodict = {}.fromkeys(('keyword', 'rank', 'rank_change','query_date'))
                try:
                    Infodict['keyword'] = list[i][0]
                except:
                    continue
                Infodict['rank'] = int(list[i][1])
                Infodict['rank_change'] = int(list[i][2])
                Infodict['query_date'] = query_date


                # Rankdict = {}.fromkeys(('keyword','rank','query_date'))
                #
                # Rankdict['keyword'] = Infodict['keyword']
                # Rankdict['rank'] = Infodict['rank']+Infodict['rank_change']
                # Rankdict['query_date'] = Infodict['query_date']

                keywordList  = []
                keywordList.append(Infodict['keyword'])
                keywordList.append(Infodict['rank']+Infodict['rank_change'])
                keywordList.append(Infodict['query_date'])
                rankList.append(keywordList)

            try:
                makeFile("/Users/Zyang/Documents/ASO/ASO_keyword/11.five/"+appName+"/",xlFile,rankList)
                print "+1"
            except:
                print "error"
                continue


start()
# list = readFile("/Users/Zyang/Documents/ASO2/驴妈妈旅游/驴妈妈旅游_关键词覆盖数据_20161006.xlsx",[])
# for i in range(1,len(list)):
#     print list[i][0]