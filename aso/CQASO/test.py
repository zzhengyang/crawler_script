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
    def getRankInfoList(self,word,page):
        json_str = json.loads(page)
        appRankInfoPerDay = []
        for i in range(len(json_str)):
            appRankInfo = []
            appWord = json_str[i]['first'].encode('utf-8').replace("'", "\'")
            searchCount = json_str[i]['second']
            priority = json_str[i]['third']

            appRankInfo.append(i+1)
            appRankInfo.append(appWord)

            appRankInfo.append(priority)
            appRankInfo.append(searchCount)
            appRankInfo.append(word)

            appRankInfoPerDay.append(tuple(appRankInfo))
        return appRankInfoPerDay
        # return rankInfoList

def apps():

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

    cur.execute("select distinct app_word from list_app")
    result = cur.fetchall()

    for word in trange(len(result)):
        #http://backend.cqaso.com/search/%E4%BD%A0%E5%A5%BD/suggestion?country=CN
        # http://backend.cqaso.com/app/1210637261/asoWord?limit=100&offset=0&pastDate=20170313&date=20170314&direction=asc,desc&field=rank,priority&country=CN&fuzzy=1
        queryURL = cqaso.siteURL + 'search/' + result[word][0] + "/suggestion?country=CN"


        # cur.execute("SELECT id FROM single_app WHERE query_date='%s' and app_word='%s' " % (sdate, appName))
        # results = cur.fetchone()
        # if results is not None:
        #     print "已存在"
        #     continue
        # else:
        try:
            page = cqaso.getPage(queryURL)

            # time.sleep(1)
            keywordInfoList = cqaso.getRankInfoList(result[word][0],page)

        except:
            print traceback.format_exc()
            print word
            continue

        try:
            stmt = "INSERT INTO image_apps(related_index,related_word,app_priority,app_searchcount,origin_word)\
                             VALUES       (%s,         %s,      %s,               %s,%s)"
            cur.executemany(stmt, keywordInfoList)
            conn.commit()

        except:
            print traceback.format_exc()
            continue

        # else:
        #     break

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

    cur.execute("select distinct app_word from single_app")
    result = cur.fetchall()

    for word in trange(3340,len(result)):
        #http://backend.cqaso.com/search/%E4%BD%A0%E5%A5%BD/suggestion?country=CN
        # http://backend.cqaso.com/app/1210637261/asoWord?limit=100&offset=0&pastDate=20170313&date=20170314&direction=asc,desc&field=rank,priority&country=CN&fuzzy=1
        queryURL = cqaso.siteURL + 'search/' + result[word][0] + "/suggestion?country=CN"


        # cur.execute("SELECT id FROM single_app WHERE query_date='%s' and app_word='%s' " % (sdate, appName))
        # results = cur.fetchone()
        # if results is not None:
        #     print "已存在"
        #     continue
        # else:
        try:
            page = cqaso.getPage(queryURL)

            # time.sleep(1)
            keywordInfoList = cqaso.getRankInfoList(result[word][0],page)

        except:
            print traceback.format_exc()
            continue

        try:
            stmt = "INSERT INTO image_app(image_word,app_priority,app_searchcount,origin_word)\
                             VALUES       (%s,      %s,               %s,%s)"
            cur.executemany(stmt, keywordInfoList)
            conn.commit()

        except:
            print traceback.format_exc()
            continue

        # else:
        #     break

    a += 1


    cur.close()
    conn.close()

if __name__ == '__main__':
    apps()
