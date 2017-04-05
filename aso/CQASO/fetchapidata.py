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

class CQASO:
    def __init__(self):
        self.siteURL = 'http://backend.cqaso.com/'
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
        self.cookies = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1ODQxMTYyZjg5ZGUyNjRmYTI0YTkxMTMiLCJjcmVhdGVkIjoxNDgwNjYwNTI4MTk0LCJleHAiOjE1MTIxOTY1Mjh9.Nrj8z8cEsJD5KWilC_I_XVk4Jrpy4XzGhLfxR8vgdVVWci2c0nJLVZItu6dhjG5uIEjMXKbzBfT5yMqRkc0_DQ'
        self.headers = {'User-Agent': self.user_agent, "X-Auth-Token": self.cookies}
    # 获得主页面html
    def getPage(self, url):
        try:

            request = urllib2.Request(url,headers=self.headers)
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
        timeRange['currentTime'] = sCurrentTime.replace("-","")
        timeRange['lastYearTime'] = sLastYearTime.replace("-","")
        return timeRange



    # 获得排名信息
    def getRankInfoList(self, appId,appName,sdate,page):
        json_str = json.loads(page)
        rankInfoList = json_str['contents']
        appRankInfoPerDay = []
        for i in rankInfoList:
            appRankInfo = []
            word = i['word'].encode('utf-8').replace("'","\'")
            rank = i['rank']
            priority = i['priority']
            searchCount = i['searchCount']
            floatRank = i['floatRank']

            appRankInfo.append(appId)
            appRankInfo.append(appName)
            appRankInfo.append(word)
            appRankInfo.append(rank)
            appRankInfo.append(priority)
            appRankInfo.append(searchCount)
            appRankInfo.append(floatRank)
            appRankInfo.append(sdate)

            appRankInfoPerDay.append(tuple(appRankInfo))
        return appRankInfoPerDay
        # return rankInfoList

def start():
    a=0
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
    # page = cqaso.getPage("http://backend.cqaso.com/topList/snapshot/20161111:1759:6003:27?limit=100&offset=0&country=CN")
    # print page
    # json_str = json.loads(page)
    # rankInfoList = json_str['contents']
    # for rankInfoNum in range(99,len(rankInfoList)):
    #     rankInfo = rankInfoList[rankInfoNum]
    #     appId = int(rankInfo['appId'].encode('utf-8'))
    #     appName = rankInfo['name'].encode('utf-8')

    cur.execute("SELECT app_id,name FROM app_info2")
    rankInfoList= cur.fetchall()
    for rankInfoNum in range(222,230):#217-230
        # print rankInfoList[rankInfoNum][1]
        rankInfo = rankInfoList[rankInfoNum]
        appId = int(rankInfo[0])
        appName = rankInfo[1].encode('utf-8')
        for day in range(0,262):
            #http://backend.cqaso.com/app/580370312/asoWord?limit=100000&offset=0&pastDate=20160201
            queryURL = "http://backend.cqaso.com/app/"+str(appId)+"/asoWord?limit=100000&offset=0&pastDate="+\
                       cqaso.getTimeRange(day+1)['lastYearTime']+"&date="\
                       +cqaso.getTimeRange(day)['lastYearTime']+"&direction=asc,desc&field=rank,priority&country=CN&fuzzy=1"

            year = cqaso.getTimeRange(day)['lastYearTime'][0:4]
            month = cqaso.getTimeRange(day)['lastYearTime'][4:6].zfill(2)
            daytime = cqaso.getTimeRange(day)['lastYearTime'][6:8].zfill(2)
            sdate = year + "-" + month + "-" + daytime

            cur.execute("SELECT id FROM keyword_day2 WHERE query_date='%s' and app_name='%s' " % (sdate, appName))
            results = cur.fetchone()
            if results is not None:
                print "已存在"
                continue
            else:
                try:
                    page = cqaso.getPage(queryURL)
                    time.sleep(2)
                    keywordInfoList = cqaso.getRankInfoList(appId,appName.replace("'"," "),sdate,page)

                except:
                    continue
                if keywordInfoList:
                # for keywordInfo in keywordInfoList:
                #     print keywordInfoList

                        try:
                            stmt = "INSERT INTO keyword_day2(app_id,app_name,app_word,app_rank,app_priority,app_searchcount,app_floatrank,query_date)\
                                                    VALUES (%s,    %s,      %s,       %s,       %s,           %s,               %s,           %s)"
                            cur.executemany(stmt, keywordInfoList)
                            conn.commit()
                            print "+"+str(len(keywordInfoList))
                        except:

                            continue


                else:
                    break
        a+=1
        print "app+"+appName
    cur.close()
    conn.close()


if __name__ == '__main__':
    start()
