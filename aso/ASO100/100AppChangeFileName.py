# coding:utf-8
import os
import re

import MySQLdb

conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            passwd='root',
            db='aso',
            port=3306,
            charset="utf8"
        )
cur = conn.cursor()
cur.execute("select app_id,name from downloadkeywordcheck")
result = cur.fetchall()
appInfo = []
fileList = []
keywordList = []
dir = "/Users/Zyang/Dropbox/ASO数据/旅游分类数据/ASO_FILE/"
for i in result:
    appInfo.append(list(i))

for s in os.listdir(dir):
    if s ==".DS_Store":
        continue
    else:
        for f in os.listdir(dir+s):
            if f==".DS_Store":
                continue
            else:
                fileList.append(f)

for i in fileList:
    try:
        if re.compile(r'_(.*?).xlsx').findall(i)[0] == "keywordyear":
            keywordList.append(i)
    except:
        continue
a=0
for i in keywordList:
    for j in appInfo:

        if i[0:3] in j[1].encode('utf8'):
            try:
                os.rename(dir +list(re.compile('^(.*?)_|^(.*?) _').findall(i)[0])[0]+"/"+i, "/Users/Zyang/Dropbox/ASO数据/旅游分类数据/ASO100_keyword_1118/" + str(j[0])+".xlsx")
            except:
                print i
                continue
            a+=1
            break
        else:

            continue
print a
#     # if (re.compile(r'_(.*?).xlsx').findall(i)[0] == "keywordyear") && ():
#         try:
#             if re.compile(r'^(.*?)_').findall(i)[0] in j[1]:
#                 print i
#         except:
#             continue