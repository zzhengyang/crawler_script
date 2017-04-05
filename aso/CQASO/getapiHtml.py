import os

import MySQLdb
import urllib2

import time

import datetime

import sys

a=0
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
authToken = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI1ODRlNmQ3NDg5ZGUyNjYzNDE2NjdhZWIiLCJjcmVhdGVkIjoxNDgxNTM0ODM2OTY4LCJleHAiOjE1MTMwNzA4MzZ9.yerAs7cdcTXeDmN9HFSZt-3OtMixIYb9rNetkO1_mUNF2SdFFacPgD0l3C9qmo-jw4ugAZJHlW-2d4JZTK30yA'
headers = {'User-Agent': user_agent, "X-Auth-Token": authToken}
conn = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='root',
        db='cq_aso',
        port=3306,
        charset="utf8"
)
cur = conn.cursor()
cur2 = conn.cursor()

def getPage(url):
    try:

        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        page = response.read()
        # pageCode = re.sub(r'<br[ ]?/?>', '\n', page)
        # return pageCode
        return page
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            print e.reason
            return None


def getTimeRange(day):
    timeRange = {}
    # sCurrentTime = time.strftime("%Y-%m-%d", time.localtime())
    sCurrentTime = '2016-12-07'
    currentTime = datetime.datetime.strptime(sCurrentTime, "%Y-%m-%d")
    lastYearTime = currentTime - datetime.timedelta(days=day)
    sLastYearTime = lastYearTime.strftime("%Y-%m-%d")
    timeRange['currentTime'] = sCurrentTime.replace("-", "")
    timeRange['lastYearTime'] = sLastYearTime.replace("-", "")
    return timeRange


cur.execute("SELECT app_id,name FROM app_info2")
rankInfoList= cur.fetchall()
for rankInfoNum in range(298,len(rankInfoList)):
    rankInfo = rankInfoList[rankInfoNum]
    appId = int(rankInfo[0])

    path = "/Users/Zyang/Documents/ASO/CQASO_html/"+str(appId)+"/"

    for day in range(0, 260):
        cur.execute("SELECT id FROM app_check WHERE query_date='%s' and app_id=%d" % (getTimeRange(day)['lastYearTime'],appId))
        results = cur.fetchone()
        if results is not None:
            print "exist"
            continue
        else:
             try:
        # print time.localtime()
        # print getTimeRange(day)
                queryURL = "http://backend.cqaso.com/app/" + str(appId) + "/asoWord?limit=100000&offset=0&pastDate=" + \
                           getTimeRange(day + 1)['lastYearTime'] + "&date=" \
                           + getTimeRange(day)['lastYearTime'] + "&direction=asc,desc&field=rank,priority&country=CN&fuzzy=1"
                page = getPage(queryURL)
                time.sleep(1)
                appPerDayHtml = open(path+getTimeRange(day)['lastYearTime']+".html",'w')
                appPerDayHtml.write(page)
                appPerDayHtml.close()
                a+=1
                cur.execute("insert into app_check(app_id,query_date) values (%d,'%s')"%(appId,getTimeRange(day)['lastYearTime']))
                conn.commit()
                print getTimeRange(day)['lastYearTime']+"===="+str(appId)
             except:
                 continue


cur.close()
conn.close()

# print getPage("http://backend.cqaso.com/app/1148524123/asoWord?limit=100&offset=0&pastDate=20161211&date=20161102&direction=asc,desc&field=rank,priority&country=CN&fuzzy=1")
# appPerDayHtml = open("/Users/Zyang/"+getTimeRange(40)['lastYearTime']+".html",'w')
# appPerDayHtml.write(page)
# appPerDayHtml.close()
