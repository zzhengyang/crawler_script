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
from tqdm import tqdm
from tqdm import trange

reload(sys)
sys.setdefaultencoding("utf-8")

class CQASO:
    def __init__(self):
        self.baseURL = 'http://sj.qq.com/myapp/cate/appList.htm'
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        self.cookies = 'session_uuid=b2c90233-4387-4ab4-a5ab-17fc6d51500f; tvfe_boss_uuid=6ff500d6d555ed13; sd_userid=56661482118040057; sd_cookie_crttime=1482118040057; o_cookie=424536312; ts_refer=www.google.com/; pgv_pvid=5640566096; ts_uid=3021200229; douyu_loginKey=047cbc9c4330e6fd715c8fb7ac2da846; verifysession=h02JuhJNPwMM-tWCmMWaCaGJGjngQlcDeZofosg2riOrA3iP5VAAkWJFCk2DP1ZD49hzii7HEzdWM3FyiSHpaMkSvgE2TkQQBPp; ptui_loginuin=846385427; ptcz=e4da2ba4ed0fe5f0f44f5aeaab5536a250d0c45c4cb6325b0204a058b15298ee; pt2gguin=o0846385427; uin=o0846385427; skey=@HzXe2XBkc; JSESSIONID=aaal6MMuZHivmhlH6FVRv'
        self.headers = {'User-Agent': self.user_agent}
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

def start():
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
    categories = [0, -10, 122, 102, 110, 103, 108, 115, 106, 101, 119, 104, 114, 117, 107, 112, 118, 111, 109, 105, 100, 113, 116]
    for i in tqdm(categories):
        b = []
        page = cqaso.getPage(cqaso.baseURL + '?orgame=1&categoryId=' + str(i) + '&pageSize=120&pageContext=0')
        json_str = json.loads(page)
        rankInfoList = json_str['obj']
        for rankInfoNum in rankInfoList:
            a = []


            appId = rankInfoNum['appId']
            categoryId = str(i)
            appName = rankInfoNum['appName'].encode('utf-8')
            appDownCount = rankInfoNum['appDownCount']
            appSize = rankInfoNum['fileSize']

            a.append(appId)
            a.append(categoryId)
            a.append(appName)
            a.append(appDownCount)
            a.append(appSize)

            st = "insert into qq_app(appId,categoryId,appName,appDownCount,appSize) values   (%s,   %s,%s,     %s,          %s)"
            cur.execute(st, (appId, categoryId, appName, appDownCount, appSize))
            conn.commit()


    cur.close()
    conn.close()

if __name__ == '__main__':
    start()
