# -*-coding:utf-8 -*-
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import ast

def data_correct():
    conn = MySQLdb.connect(
        host='47.93.113.252',
        user='dev',
        passwd='lotus',
        db='dtrip',
        port=3306,
        charset="utf8"
    )
    cur = conn.cursor()
    cur.execute("select id,photo_urls,description,phone,office_hours from merchants")
    result = cur.fetchall()
    for i in result:
        content = ast.literal_eval(i[1])[0]
        correctPhone = i[3].replace(' ','')
        correctHours = i[4].replace("：", ":")
        addHtml = '<head><style type="text/css">body {margin: 0; padding: 0; outline: 0 none; background-color: rgb(34, 34, 34)}p {font-family: "PingFangSC-Light";line-height: 33px;font-size: 16px;font-weight: inherit;font-weight: 200}</style></head>'
        originalDescription = i[2].replace(addHtml,'').replace('rgb(136, 136, 136)','rgb(187, 187, 187)')
        darkDescription = addHtml  + originalDescription
        # cur.execute("update merchants set content_image_url= '%s',description= '%s',phone= '%s',office_hours= '%s' where id= %d" % (content, originalDescription, correctPhone, correctHours, i[0]))
        cur.execute("update merchants set content_image_url= '%s',description= '%s',phone= '%s',office_hours= '%s' where id= %d"%(content,darkDescription,correctPhone,correctHours,i[0]))
        conn.commit()
        print darkDescription+'\n'

def feeds_sort(list):
    conn = MySQLdb.connect(
        host='47.93.113.252',
        user='dev',
        passwd='lotus',
        db='dtrip',
        port=3306,
        charset="utf8"
    )
    cur = conn.cursor()
    a = 0
    for id in list:
        cur.execute("update feeds set weight=%d where related_id=%d"%(a,id))
        conn.commit()
        print a
        a+=1
# data_correct()
feeds_sort([18,20,19,11,21,6,22,16,4,3,5,2])
# result = cur.fetchall()
# for i in result:
#
#     cur.execute("update merchants set weight=%d
#     conn.commit()
