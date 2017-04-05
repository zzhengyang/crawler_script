# coding=utf-8
import traceback

import MySQLdb
import sys
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
cur.execute("SELECT DISTINCT query_date FROM keyword_html")
dateResult = cur.fetchall()
cur.execute("SELECT DISTINCT app_id FROM keyword_html")
idResult = cur.fetchall()
cur.execute("SELECT app_word FROM keyword_html")
keywordResult1 = cur.fetchall()

# keywordResult = []
# data = xlrd.open_workbook("/Users/Zyang/Documents/ASO/oneyearkeyword/keyword_list.xlsx")
# table = data.sheet_by_index(0)
# nrows = table.nrows
# for i in range(2, nrows):
#     a = table.row_values(i)
#     if not a[0]:
#         continue
#     keywordResult.append(a)

#获得keywordlist文件
keywordResult = list(set(keywordResult1))
w = xlsxwriter.Workbook(path_des + "keyword_list"+".xlsx")
ws = w.add_worksheet('keyword')
keyDict = {}
for i in range(len(keywordResult)):
    key = keywordResult[i][0]
    if not keyDict.has_key(key):
        keyDict[key] = i

        ws.write(i,0,key)
w.close()

# print keyDict.has_key('air')        #True
# print keyDict.has_key(' air ')
# print keyDict.has_key(' air')       #True
# print keyDict.has_key('air ')
# print keyDict.has_key('  air  ')    #True
# print keyDict.has_key('  air ')
# print keyDict.has_key(' air  ')

#获得day文件
# for j in range(len(dateResult)):
#     w = xlsxwriter.Workbook(path_des + "Day"+str(j+1).zfill(3)+".xlsx")
#     ws = w.add_worksheet('aso')
#     for id in range(len(idResult)):
#         try:
#             cur.execute("SELECT app_rank, app_word from keyword_html where app_id=%d and query_date='%s'" % (idResult[id][0], str(dateResult[j][0])))
#             appRank = cur.fetchall()
#             for key in appRank:
#                # print key
#                 ws.write(keyDict[key[1]],id,key[0])
#         except:
#
#             traceback.print_exc()
#             continue
#
#     w.close()
#     print "Day"+str(j+1).zfill(3)

cur.close()
conn.close()