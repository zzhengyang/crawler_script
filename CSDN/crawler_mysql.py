#coding:utf-8
import MySQLdb

'''
import crawler_MFW


mfw = crawler_MFW.MFW('曼谷')
a = mfw.saveFood()
'''

name = 'nihao'
enname = "你好"

try:
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='TourApp', port=3306)
    cur = conn.cursor()

    cur.execute('INSERT INTO Category(id,name,enname) VALUES(NULL ,name,enname)')
    conn.commit()
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
