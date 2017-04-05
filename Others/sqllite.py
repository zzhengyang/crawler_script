#coding:utf-8
import MySQLdb

conn = MySQLdb.connect(
    host='139.129.218.173',
    user='dev',
    passwd='123456',
    db='dtrip',
    port=3306,
    charset="utf8"
)
a = []
cnList = []
cur = conn.cursor()
cur.execute("select id FROM merchants where status=3")
cnResult = cur.fetchall()
for i in cnResult:
    cur.execute("select id from products where merchant_id=%d"%i[0])
    proResult = cur.fetchall()
    if not proResult:
        cur.execute("select id,avgprice from merchants where id =%d"%int(i[0]))
        result = cur.fetchall()
        for j in result:
            if int(j[1]) == 0:
                continue
            print j[0],str(int(j[1]))+"THB"
            cur.execute("insert into products(merchant_id,price,lang) values(%s,%s,%s)",(j[0],str(int(j[1]))+"THB","zh-CN"))
            conn.commit()
cur.close()
conn.close()
        # cur.execute("insert into ")
    # cur.execute("insert into merchant_categories(merchant_id,category_id) values(%s,%s)",(i[0],46))
    # conn.commit()
# conn1 = MySQLdb.connect(
#     host='139.129.218.173',
#     user='dev',
#     passwd='123456',
#     db='dtrip',
#     port=3306,
#     charset="utf8"
# )
# cur1 = conn1.cursor()
# for i in cnResult:
#     cur1.execute('INSERT INTO events_test "'+i+'"')

