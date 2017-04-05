# -*- coding: utf-8 -*-
import traceback

import MySQLdb
import sys

import datetime
import xlrd
import xlsxwriter

conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            passwd='root',
            db='cq_aso',
            port=3306,
            charset="utf8"
        )
cur = conn.cursor()
path_des = "/Users/Zyang/Documents/ASO/dropFile/"
print "开始数据获取"
starttime = datetime.datetime.now()
cur.execute("SELECT DISTINCT query_date FROM keyword_old")
dateResult = cur.fetchall()
cur.execute("SELECT DISTINCT app_id FROM keyword_old")
idResult = cur.fetchall()
cur.execute("SELECT  app_word FROM keyword_old")
keywordResult1 = cur.fetchall()
print "数据库数据获取完成"
endtime = datetime.datetime.now()
print (endtime - starttime).seconds
cur.close()
cur = conn.cursor()
# keywordResult = []
# data = xlrd.open_workbook("/Users/Zyang/Documents/ASO/oneyearkeyword/keyword_list.xlsx")
# table = data.sheet_by_index(0)
# nrows = table.nrows
# for i in range(2, nrows):
#     a = table.row_values(i)
#     if not a[0]:
#         continue
#     keywordResult.append(a)
keywordResult = list(set(keywordResult1))
# w = xlsxwriter.Workbook(path_des + "keyword_list"+".xlsx")
# ws = w.add_worksheet('keyword')
# for i in range(0,len(keywordResult)):
#     ws.write(i,0,keywordResult[i][0])
# w.close()
keyDict = {}
unkeyDict = {}
for i in range(len(keywordResult)):
    key = keywordResult[i][0]
    if not keyDict.has_key(key):
        keyDict[key] = i
        unkeyDict[i] = key
# print keyDict.has_key('air')        #True
# print keyDict.has_key(' air ')
# print keyDict.has_key(' air')       #True
# print keyDict.has_key('air ')
# print keyDict.has_key('  air  ')    #True
# print keyDict.has_key('  air ')
# print keyDict.has_key(' air  ')
w = xlsxwriter.Workbook(path_des + "app_searchcount"+".xlsx")
ws = w.add_worksheet('searchcount')
for j in range(len(dateResult)):


    for keyword in range(len(keyDict)):
            priority = 0

            # print keyword
            # print unkeyDict[keyword].encode('utf-8').replace("'","\\'"), dateResult[j][0].encode('utf-8')
            try:
                cur.execute("SELECT app_searchcount from keyword_old where app_word='%s' and query_date= '%s' limit 1" \
                            % (unkeyDict[keyword].encode('utf-8').replace("'", "\\'"), dateResult[j][0].encode('utf-8')))
                appPriorities = cur.fetchall()
                # print appPriorities[0][0]

                # for appPriority in appPriorities:
                #     if appPriority[0] <> 0:
                #
                #         priority += appPriority[0]

            except:
                # print unkeyDict[keyword]
                traceback.print_exc()
                continue

            try:
                # avgPriority = priority/len(appPriorities)
                if appPriorities[0][0] <> 0:
                    ws.write(keyword, j, appPriorities[0][0])
                else:
                    continue
            except :

                continue



    print "Day"+str(j+1).zfill(3)
w.close()
cur.close()
conn.close()