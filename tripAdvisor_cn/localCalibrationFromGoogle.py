#coding:utf8

import time
import datetime
import re
import traceback
import urllib2
import sys
from decimal import Decimal
import math

import MySQLdb
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")
header={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',\
        'Cookie':'NID=89=nzsEa7Dk_PFAKRlT2y7cX61ar0kwSiqEqazflLtcIXNd97RzWb8dCwN3HqgUr3hL0VqnkRUNA-NCl6GnXFAm2eaD3zjEA1jx0Stm0WbThA1WvNYCX2fIx9QImhbaKLgl',\
        }
conn = MySQLdb.connect(
    host='139.129.218.173',
    user='dev',
    passwd='123456',
    db='dtrip',
    port=3306,
    charset="utf8"
)
cur = conn.cursor()
cur.execute("select id,name,ST_X(coordinate),ST_Y(coordinate),city_id,category_id from merchants")
queryResultListFromDb = cur.fetchall()
def getPage(url):
    try:

        request = urllib2.Request(url,headers=header)
        response = urllib2.urlopen(request)
        page = response.read()
        # pageCode = re.sub(r'<br[ ]?/?>', '\n', page)
        # return pageCode
        return page
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            print e.reason
            return None

def getLocal(page):
    googleLocal = []
    lnt = re.findall('APP_INITIALIZATION_STATE.*?,(.*?),(.*?)]',page)[0][0]
    lat = re.findall('APP_INITIALIZATION_STATE.*?,(.*?),(.*?)]', page)[0][1]
    googleLocal.append(round(float(lnt),6))
    googleLocal.append(round(float(lat),6))
    return googleLocal
illegalLocalMerchants = []
for i in queryResultListFromDb:

    querySite = "http://www.google.cn/maps/search/"+str(i[1]).replace(" ","%20")+"?hl=zh-CN"
    try:
        gLocal = getLocal(getPage(querySite))
    except:
        continue
    X_Local = abs(Decimal(i[2])-Decimal(gLocal[0]))
    Y_Local = abs(Decimal(i[3])-Decimal(gLocal[1]))
    # print i[1]
    # print "经度差: "+str(X_Local)
    # print "纬度差: " +str(Y_Local)
    # print '\n'
    if (round(X_Local,2)>0.00 and round(Y_Local,2)>0.00):
        print "城市id:"+str(i[4])+" "+"分类id:"+str(i[5])+" "+"店铺id:"+str(i[0])+" "+i[1]
        print "Google经度 "+ str(gLocal[0])
        print "Google纬度 "+ str(gLocal[1])
        print "App经度 "+ str(i[2])
        print "App纬度 "+ str(i[3])
        print "\n"
        # illegalLocalMerchants.append(i[0])
# print illegalLocalMerchants
# page = getPage("http://www.google.cn/maps/search/Bangkok%20Float%20Center?hl=zh-CN")
# print getLocal(page)
# print page