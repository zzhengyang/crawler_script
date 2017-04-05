# coding:utf-8
import json
import time
import datetime
import re
import traceback
import urllib2
import sys

import MySQLdb


city_id=1
def getPage(url):
    try:

        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        page = response.read()
        pageCode = re.sub(r'<br[ ]?/?>', '\n', page)
        return pageCode
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            print e.reason
            return None
def parseJson(page):
    itemJson = json.loads(page,strict=False)
    return itemJson
category_id = []
page =  getPage("https://api.dev.heylotus.com/categories?&city_id="+str(city_id))
item = parseJson(page)
for i in item:
    category_id.append(i['id'])
a = []
for id in category_id:
    print id
    merchant_page = getPage("https://api.dev.heylotus.com/merchants?city_id="+str(city_id)+"&category_id="+str(id)+"&sort=distance&_coordinate=2,2&status=3")
    merchantsJson = parseJson(merchant_page)
    if len(merchantsJson['items'])>0:
        a.append((id,city_id))
    # print merchantsJson['current_page']
print a