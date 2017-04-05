# coding:utf-8
import re
import time
import webbrowser
import datetime
from urllib import quote
import urllib2
import MySQLdb
from bs4 import BeautifulSoup
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class ASO100:
    def __init__(self):
        self.siteURL = 'http://aso100.com'
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        self.cookies = 'nt_r=1; nt_r_ov=1; optimiza=58097b48ca664516; USERINFO=7iI5hYLyYCQ1dfpJJjlRdjlH31c%2F7lHba4XCdMq3q7t2bYffDQ6vht24KPy6U1DsvN6vQTE6lLg%3D; PHPSESSID=i3ahiv09t7m3u2kgisc71fj1f1; s1019=1477324799000; Hm_lvt_0bcb16196dddadaf61c121323a9ec0b6=1477018483,1477018494,1477020566,1477277061; Hm_lpvt_0bcb16196dddadaf61c121323a9ec0b6=1477277061'
        self.headers = {'User-Agent': self.user_agent, "cookie": self.cookies}

    # 获得主页面html
    def getPage(self, url):
        try:

            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            page = response.read()
            pageCode = re.sub(r'<br[ ]?/?>', '\n', page)
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

    # 获得店铺页面链接
    def getHref(self, page):
        # rankURL = "/rank/index/device/iphone/country/cn/brand/free/genre/6003"
        # page = self.getPage(self.siteURL + rankURL)
        soup = BeautifulSoup(page, 'html.parser')
        href = []
        items = soup.find("div", class_="rank-list").find_all("div", class_="row")
        for item in items:
            appCols = item.find_all("div", class_="col-md-2")
            for appCol in appCols:
                tag = []
                tag.append(appCol.a['href'])
                tag.append(str(appCol.img['alt']).split('.')[0])
                href.append(tag)
        return href

    def getAppId(self, detailURL):
        app_id = re.findall(re.compile('appid/(.*?)/country'), detailURL)
        return app_id[0]

    # def getAppClassRank(self,page):
    #     soup = BeautifulSoup(page,'html.parser')



    # 获得app标题
    def getAppTitle(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        return soup.find("div", class_="appinfo-body").h3.getText()

    # 获得时间范围
    def getTimeRange(self, day):
        timeRange = {}
        sCurrentTime = time.strftime("%Y-%m-%d", time.localtime())
        currentTime = datetime.datetime.strptime(sCurrentTime, "%Y-%m-%d")
        lastYearTime = currentTime - datetime.timedelta(days=day)
        sLastYearTime = lastYearTime.strftime("%Y-%m-%d")
        timeRange['currentTime'] = sCurrentTime
        timeRange['lastYearTime'] = sLastYearTime
        return timeRange

    def start(self):

        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            passwd='root',
            db='aso',
            port=3306,
            charset="utf8"
        )
        cur = conn.cursor()
        print "更新中..."
        a = 0
        for i in range(200, 365):
            queryDate = self.getTimeRange(i)['lastYearTime']
            # http://aso100.com/rank/index/device/iphone/country/cn/brand/free/genre/6003/date/2016-10-20
            url = "http://aso100.com/rank/index/device/iphone/country/cn/brand/free/genre/6003/date/" + queryDate
            page = self.getPage(url)
            hrefs = self.getHref(page)

            soup = BeautifulSoup(page, 'html.parser')
            classrank = soup.find()
            hrefList = [hrefs[i] for i in range(0, 100)]
            for href in hrefList:
                appID = self.getAppId(href[0])
                classrank = href[1]

                print classrank, appID

                # try:
                cur.execute("update information set class_rank='%s' where query_date = '%s'  and app_id = '%d'" \
                            % (int(classrank), queryDate, int(appID)))
                conn.commit()



                # except:
                #     a += 1
                #     print "更新失败"
                #     continue
                a += 1
                print "更新成功第" + str(a) + "条"

        cur.close()
        conn.close()
        print "抓取完成，共" + str(a) + "条记录"


aso = ASO100()
aso.start()
# url = "http://aso100.com/rank/index/device/iphone/country/cn/brand/free/genre/6003/date/2016-10-5"
# page = aso.getPage(url)
# hrefs = aso.getHref(page)
# print hrefs





# aso.downLoadRank(appID, rankPage)
# time.sleep(5)
#
# commentPage = aso.getDetailPage("commentList", appID)
# aso.downLoadComment(appID, commentPage)
# time.sleep(5)
#
# keyWordPage = aso.getDetailPage("keyword", appID)
# aso.downLoadKeyWord(appID, keyWordPage)
# time.sleep(5)
