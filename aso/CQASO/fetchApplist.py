# coding:utf-8
import json
import time
import datetime
import re
import traceback
import urllib2
import sys

import MySQLdb

reload(sys)
sys.setdefaultencoding("utf-8")

conn = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='root',
        db='cq_aso',
        port=3306,
        charset="utf8"
    )
cur = conn.cursor()



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


def getTimeRangeNoSymbol(day):
    timeRange = {}
    sCurrentTime = time.strftime("%Y-%m-%d", time.localtime())
    currentTime = datetime.datetime.strptime(sCurrentTime, "%Y-%m-%d")
    lastYearTime = currentTime - datetime.timedelta(days=day)
    sLastYearTime = lastYearTime.strftime("%Y-%m-%d")
    timeRange['currentTime'] = sCurrentTime.replace("-", "")
    timeRange['lastYearTime'] = sLastYearTime.replace("-", "")
    return timeRange

for day in range(0,270):#270
    appInfoList = []
    fetchDate = getTimeRangeNoSymbol(day)['lastYearTime']
    datePage = getPage("http://backend.cqaso.com/topList/snapshot/"+fetchDate+"/6003/27?country=CN")
    json_date = json.loads(datePage)
    argDate = json_date[0]['y']
    time.sleep(2)
    appListPage = getPage("http://backend.cqaso.com/topList/snapshot/"+argDate+"?limit=100&offset=0&country=CN")
    json_str = json.loads(appListPage)
    rankInfoList = json_str['contents']
    for rankInfoNum in range(0, len(rankInfoList)):
        rankInfo = rankInfoList[rankInfoNum]
        appId = int(rankInfo['appId'].encode('utf-8'))
        appName = rankInfo['name'].encode('utf-8')
        cur.execute("SELECT id FROM app_info2 where app_id=%d"%appId)
        results = cur.fetchone()
        if results is not None:
            continue
        else:
            appInfoList.append((appId,appName))
    insertSql = "INSERT INTO app_info2(app_id,name) VALUES (%s,%s)"
    cur.executemany(insertSql,appInfoList)
    conn.commit()
    print "day: "+fetchDate +"   insertNum: "+str(len(appInfoList))
cur.close()
conn.close()