# coding=utf-8
import json
import re

import MySQLdb
import xlrd


def get_median(data):
    data.sort()
    half = len(data) // 2
    return (data[half] + data[~half]) / 2

conn1 = MySQLdb.connect(
    host='127.0.0.1',
    user='root',
    passwd='root',
    db='dtrip',
    port=3306,
    charset="utf8"
)
cur1 = conn1.cursor()
cur1.execute("SELECT merchant_id,author_name,content,shop_id FROM comments_en")
enCommentsResult = cur1.fetchall()
conn = MySQLdb.connect(
    host='139.129.218.173',
    user='dev',
    passwd='123456',
    db='dtrip',
    port=3306,
    charset="utf8"
)
# merchantList = []
cur = conn.cursor()
for i in enCommentsResult:
    cur.execute("SELECT * FROM comments WHERE merchant_id=%d" % int(i[0]))
    results = cur.fetchone()
    if results is not None:
        print "已存在"
        continue
    else:
        try:
            cur.execute("insert into comments(merchant_id,author_name,content,shop_id,lang) VALUES (%d,'%s','%s',%d,'%s')"%\
                    (i[0],i[1].encode('utf8'),i[2].encode('utf8'),i[3],'en-US'))
            conn.commit()
        except:
            continue
# print merchantList
# for i in localResult:
#     dict = {}.fromkeys(['author_name', 'content'])
#     dict['author_name'] = i[1].encode('utf8').replace('"', '').replace("'", "")
#     dict['content'] = i[2].encode('utf8').replace('"', '').replace("'", "")
#
#     jsonStr = json.dumps(dict)
#     cur.execute("INSERT INTO translations(owner_type,owner_id,data,lang) VALUES ('%s',%d,'%s','%s')" % ( \
#         UPDATE_TYPE, int(i[0]), jsonStr, LANG ))
#     # conn.commit()
#     print jsonStr
#     print i[0]
#
cur1.close()
conn1.close()
cur.close()
conn.close()
