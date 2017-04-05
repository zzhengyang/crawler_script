# coding=utf-8
import MySQLdb

conn = MySQLdb.connect(
    host='139.129.218.173',
    user='dev',
    passwd='123456',
    db='dtrip',
    port=3306,
    charset="utf8"
)
cur = conn.cursor()
a=0
cur.execute("SELECT id FROM merchants where category_id =6 and city_id between 1 and 4")
merchantResult = cur.fetchall()
for i in merchantResult:
    cur.execute("select * from merchant_categories where merchant_id=%d "% i[0])
    results = cur.fetchone()

    if results is not None:
        print "已存在"+str(i[0])
        continue
    else:
        cur.execute("INSERT INTO merchant_categories(merchant_id,category_id) values(%d,%d)"%(int(i[0]),45))
        conn.commit()
        a+=1
        print str(i[0])
print a
cur.close()
conn.close()