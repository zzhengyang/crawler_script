# coding:utf-8
import os
import re

import MySQLdb
import xlrd

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

def start():
    conn = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='root',
        db='aso',
        port=3306,
        charset="utf8"
    )
    cur = conn.cursor()
    srcPath = "/Users/Zyang/Documents/ASO2/"
    dirList = GetFileList(srcPath,[])
    for appName in dirList:
        cur.execute("SELECT id FROM keyword WHERE app_name =" + appName + "")
        results = cur.fetchone()

        if results is not None:
            print "已存在"
            continue
        else:
            for xlFile in  os.listdir(srcPath+appName):
                if xlFile == ".DS" or xlFile == ".DS_Store":
                    continue
                # print srcPath+appName+"/"+xlFile
                query_date = re.compile(r'_(\d+)').findall(xlFile)[0]
                list = readFile(srcPath+appName+"/"+xlFile,[])

                for i in range(1,len(list)):
                    Infodict = {}.fromkeys(('app_name','keyword', 'rank', 'rank_change', 'key_index', 'result_search','query_date'))
                    try:
                        Infodict['keyword'] = list[i][0].encode("utf8")
                    except:
                        continue
                    Infodict['rank'] = int(list[i][1])
                    Infodict['rank_change'] = int(list[i][2])
                    Infodict['key_index'] = int(list[i][3])
                    Infodict['result_search'] = int(list[i][4])
                    Infodict['query_date'] = query_date
                    Infodict['app_name'] = appName
                    print Infodict
                    cur.execute("INSERT INTO keyword(app_name,keyword,rank,rank_change,key_index,result_search,query_date)\
                                              VALUES ( '%s'   ,'%s'  ,%d  ,%d         ,%d   ,%d           ,'%s');"%\
                                (Infodict['app_name'],Infodict['keyword'],Infodict['rank'],Infodict['rank_change']\
                                     ,Infodict['key_index'],Infodict['result_search'],Infodict['query_date']))
                    conn.commit()
    cur.close()
    conn.close()
start()
# list = readFile("/Users/Zyang/Documents/ASO2/驴妈妈旅游/驴妈妈旅游_关键词覆盖数据_20161006.xlsx",[])
# for i in range(1,len(list)):
#     print list[i][0]