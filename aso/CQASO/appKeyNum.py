# coding:utf-8
import MySQLdb

conn = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='root',
        db='cq_aso',
        port=3306,
        charset="utf8"
    )
cur = conn.cursor()
cur.execute("SELECT distinct app_name from keyword_day2")
appNameList = cur.fetchall()
a = []
for i in appNameList:
    a.append(list(i)[0].encode('utf8'))

for j in a:
    cur.execute("SELECT count(*) from keyword_day2 where app_name='%s'"%str(j))
    fetchNum = cur.fetchone()

    # if int(list(fetchNum)[0])<int(2000):
    #     print str(j)+"===="+str(list(fetchNum)[0])
    # else:
    #     continue
    print str(j) + "====" + str(list(fetchNum)[0])