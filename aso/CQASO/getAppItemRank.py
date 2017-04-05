# coding:utf-8
import json
import time
import datetime
import re
import traceback
import urllib2
import sys

import MySQLdb
import xlsxwriter

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

# 获取app类别排名
def getAppItemRank():
    for day in range(5,265):
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

            cur.execute("SELECT id FROM app_rank where app_id=%d and query_date='%s'"%(appId,fetchDate))
            results = cur.fetchone()
            if results is not None:
                print "已存在"
                continue
            else:
                appInfoList.append((appId,rankInfoNum+1,fetchDate))
        insertSql = "INSERT INTO app_rank(app_id,app_item_rank,query_date) VALUES (%s,%s,%s)"
        cur.executemany(insertSql,appInfoList)
        conn.commit()
        print appInfoList
        print "day: "+fetchDate +"   insertNum: "+str(len(appInfoList))


# 生成排名文件
def proAppItemRank():
    w = xlsxwriter.Workbook("/Users/Zyang/Documents/ASO/dropFile/item_rank2.xlsx")
    ws = w.add_worksheet('rank')
    appIdList = []
    queryDateList = []
    cur.execute("SELECT distinct app_id from keyword_old")
    appList = cur.fetchall()
    for appId in appList:
        appIdList.append(int(appId[0]))
    cur.execute("SELECT distinct query_date from app_rank")
    queryDate = cur.fetchall()
    for queryDate in queryDate:
        queryDateList.append(int(queryDate[0]))

    for x in range(len(appIdList)):

        for y in range(len(queryDateList)):
            cur.execute("SELECT app_item_rank FROM app_rank WHERE app_id=%d AND query_date='%s'"%(appIdList[x],queryDateList[y]))
            appRank = cur.fetchone()
            # print appIdList[x]
            # print queryDateList[y]
            if appRank:
                # print appRank[0]
                ws.write(x,y,appRank[0])
            else:
                continue

    w.close()
# getAppItemRank()
# proAppItemRank()
appIdList = []
rankList=[]
cur.execute("SELECT distinct app_id from keyword_old")
appList = cur.fetchall()
for appId in appList:
    appIdList.append(int(appId[0]))

cur.execute("SELECT distinct app_id FROM app_rank")
appRank = cur.fetchall()
for appId in appRank:
    rankList.append(int(appId[0]))
for i in appIdList:
    if i not in rankList:
        print i
cur.close()
conn.close()