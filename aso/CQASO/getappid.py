import json
import re
import urllib2

import MySQLdb
from bs4 import BeautifulSoup


def getPage(url):
    try:

        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        page = response.read()
        # pageCode = re.sub(r'<br[ ]?/?>', '\n', page)
        # return pageCode
        return page
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            print e.reason
            return None


def getAppId(detailURL):
    app_id = re.findall(re.compile('appid/(.*?)/country'), detailURL)
    return app_id[0]


conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            passwd='root',
            db='cq_aso',
            port=3306,
            charset="utf8"
        )
cur = conn.cursor()
page = getPage("http://backend.cqaso.com/topList/6003/27?limit=100&offset=0&country=CN")
json_str = json.loads(page)
rankInfoList = json_str['contents']
for i in rankInfoList:
    appInfoList = []
    appInfoList.append(i['appId'].encode('utf-8'))
    appInfoList.append(i['name'].encode('utf-8'))
    # print type(intappInfoList[0])
    cur.execute("INSERT INTO app_info(app_id,name) VALUES (%d,'%s')"%(int(appInfoList[0]),appInfoList[1]))
    conn.commit()

cur.close()
conn.close()