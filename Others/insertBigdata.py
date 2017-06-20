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
cur.execute("select * from topics where id =166")
result = cur.fetchall()
for i in result:
    print i[0],i[3],i[8]
    cur.execute("insert into feeds(city_id,photo_url,related_type,related_id,weight,status) values(%s,%s,%s,%s,%s,%s)",(int(i[3]),i[8],'topics',int(i[0]),1,2))
    conn.commit()
print "ok"