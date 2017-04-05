# coding:utf-8
import json
import os
import time
import datetime
import re
import traceback
import urllib2
import sys

import MySQLdb

reload(sys)
sys.setdefaultencoding("utf-8")
from tqdm import trange


class CQASO:
    def __init__(self):
        self.siteURL = 'http://backend.cqaso.com/'
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
        self.auth_token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1ODIxOGQ4MTg5ZGUyNjAyNjhmODBhOTEiLCJjcmVhdGVkIjoxNDg5NDYxODgzOTA2LCJleHAiOjE1MjA5OTc4ODN9.KgbVHdrGpzSqOtqdeK81UAuyBbhU3DeFhyzFmn1Ml2mYEll5Ls4Fx1TzWzg_CG7zyEDSqlOE61IIt114LGiRAw'
        self.headers = {'User-Agent': self.user_agent, "X-Auth-Token": self.auth_token}


    # 获得主页面html
    def getPage(self, url):
        try:

            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            page = response.read()
            # pageCode = re.sub(r'<br[ ]?/?>', '\n', page)
            # return pageCode
            return page
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

    # 获得url时间范围

    def getTimeRange(self, day):
        timeRange = {}
        sCurrentTime = time.strftime("%Y-%m-%d", time.localtime())
        currentTime = datetime.datetime.strptime(sCurrentTime, "%Y-%m-%d")
        lastYearTime = currentTime - datetime.timedelta(days=day)
        sLastYearTime = lastYearTime.strftime("%Y-%m-%d")
        timeRange['currentTime'] = sCurrentTime.replace("-", "")
        timeRange['lastYearTime'] = sLastYearTime.replace("-", "")
        return timeRange

    # 获得排名信息
    def getRankInfoList(self, appId, appName, sdate, page):
        json_str = json.loads(page)
        rankInfoList = json_str['contents']
        appRankInfoPerDay = []
        for i in rankInfoList:
            appRankInfo = []
            word = i['word'].encode('utf-8').replace("'", "\'")
            rank = i['rank']
            priority = i['priority']
            searchCount = i['searchCount']
            floatRank = i['floatRank']
            if priority >= 7000:
                appRankInfo.append(appId)
                appRankInfo.append(appName)
                appRankInfo.append(word)
                appRankInfo.append(rank)
                appRankInfo.append(priority)
                appRankInfo.append(searchCount)
                appRankInfo.append(floatRank)
                appRankInfo.append(sdate)

                appRankInfoPerDay.append(tuple(appRankInfo))
            else:
                break
        return appRankInfoPerDay
        # return rankInfoList

def apps(keyword):

    a = 0
    conn = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='root',
        db='cq_aso',
        port=3306,
        charset="utf8"
    )
    cur = conn.cursor()
    cqaso = CQASO()

    appListPage = cqaso.getPage('http://backend.cqaso.com/search/' + keyword + '?sortBy=nature&limit=10&offset=0&country=CN')

    json_str = json.loads(appListPage)
    appInfoList = json_str['contents']
    appList = []
    for app in appInfoList:
        appList.append([app['appid'],app['name']])
    for app in trange(len(appList)):
        appId = appList[app][0]
        appName = appList[app][1]

        day = 0
        # http://backend.cqaso.com/app/1035505740/asoWord?limit=100&offset=0&pastDate=20170313&date=20170314&direction=desc,desc&field=priority,rank&country=CN&fuzzy=1

        queryURL = "http://backend.cqaso.com/app/" + str(appId) + "/asoWord?limit=100&offset=0&pastDate=" + \
                   cqaso.getTimeRange(day + 1)['lastYearTime'] + "&date=" \
                   + cqaso.getTimeRange(day)[
                       'lastYearTime'] + "&direction=desc,desc&field=priority,rank&country=CN&fuzzy=1"
        year = cqaso.getTimeRange(day)['lastYearTime'][0:4]
        month = cqaso.getTimeRange(day)['lastYearTime'][4:6].zfill(2)
        daytime = cqaso.getTimeRange(day)['lastYearTime'][6:8].zfill(2)
        sdate = year + "-" + month + "-" + daytime

        # cur.execute("SELECT id FROM single_app WHERE query_date='%s' and app_word='%s' " % (sdate, appName))
        # results = cur.fetchone()
        # if results is not None:
        #     print "已存在"
        #     continue
        # else:
        try:
            page = cqaso.getPage(queryURL)

            time.sleep(1)
            keywordInfoList = cqaso.getRankInfoList(appId, appName.replace("'", " "), sdate, page)
        except:
            continue
        if keywordInfoList:

            try:
                stmt = "INSERT INTO list_app(app_id,app_name,app_word,app_rank,app_priority,app_searchcount,app_floatrank,query_date)\
                                                                                VALUES (%s,    %s,      %s,       %s,       %s,           %s,               %s,           %s)"
                cur.executemany(stmt, keywordInfoList)
                conn.commit()

            except:
                print traceback.format_exc()
                continue
        else:
            break


        a += 1


    cur.close()
    conn.close()


def app():

    a = 0
    conn = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='root',
        db='cq_aso',
        port=3306,
        charset="utf8"
    )
    cur = conn.cursor()
    cqaso = CQASO()


    appId = 1210637261
    appName = '星星爱消除-最萌'
    for day in trange(0, 7):
        #http://backend.cqaso.com/app/1210637261/asoWord?limit=100&offset=0&pastDate=20170313&date=20170314&direction=desc,desc&field=floatRank,rank&country=CN&fuzzy=1
        # http://backend.cqaso.com/app/1210637261/asoWord?limit=100&offset=0&pastDate=20170313&date=20170314&direction=asc,desc&field=rank,priority&country=CN&fuzzy=1
        queryURL = "http://backend.cqaso.com/app/" + str(appId) + "/asoWord?limit=5000&offset=0&pastDate=" + \
                   cqaso.getTimeRange(day + 1)['lastYearTime'] + "&date=" \
                   + cqaso.getTimeRange(day)[
                       'lastYearTime'] + "&direction=asc,desc&field=rank,priority&country=CN&fuzzy=1"
        year = cqaso.getTimeRange(day)['lastYearTime'][0:4]
        month = cqaso.getTimeRange(day)['lastYearTime'][4:6].zfill(2)
        daytime = cqaso.getTimeRange(day)['lastYearTime'][6:8].zfill(2)
        sdate = year + "-" + month + "-" + daytime

        # cur.execute("SELECT id FROM single_app WHERE query_date='%s' and app_word='%s' " % (sdate, appName))
        # results = cur.fetchone()
        # if results is not None:
        #     print "已存在"
        #     continue
        # else:
        try:
            page = cqaso.getPage(queryURL)

            time.sleep(1)
            keywordInfoList = cqaso.getRankInfoList(appId, appName.replace("'", " "), sdate, page)
        except:
            continue
        if keywordInfoList:

            try:
                stmt = "INSERT INTO single_app(app_id,app_name,app_word,app_rank,app_priority,app_searchcount,app_floatrank,query_date)\
                                                                VALUES (%s,    %s,      %s,       %s,       %s,           %s,               %s,           %s)"
                cur.executemany(stmt, keywordInfoList)
                conn.commit()

            except:
                print traceback.format_exc()
                continue
        else:
            break

    a += 1


    cur.close()
    conn.close()

if __name__ == '__main__':
    apps('航海')
    # apps('数独')