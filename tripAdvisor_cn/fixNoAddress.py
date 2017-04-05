# coding:utf-8
import re
import time
from urllib import quote
import urllib2
import MySQLdb
from bs4 import BeautifulSoup
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
headers = {'User-Agent': user_agent}

conn = MySQLdb.connect(
    host='139.129.218.173',
    user='dev',
    passwd='123456',
    db='dtrip',
    port=3306,
    charset="utf8"
        )
cur = conn.cursor()

def getAdress(page):
    soup = BeautifulSoup(page, 'html.parser')
    address = soup.find("span",class_="format_address").getText()
    return address

def getPage(url):
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        page = response.read()
        pageCode = re.sub(r'<br[ ]?/?>', '\n', page)
        return pageCode
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            print e.reason
            return None
cur.execute('SELECT shop_id FROM merchants where address=""')
result = cur.fetchall()
for i in result:
    page = getPage("http://www.tripadvisor.cn/Attraction_Review-g293916-d"+str(i[0])+".html")
    fixAdress =  getAdress(page).replace("地址: ","")
    print fixAdress+"===="+str(i[0])
    cur.execute("update merchants set address='%s' where shop_id=%d" % (fixAdress,int(i[0])))
    conn.commit()
cur.close()
conn.close()
# print getPage("http://www.tripadvisor.cn/Attraction_Review-g293916-d8851170.html")