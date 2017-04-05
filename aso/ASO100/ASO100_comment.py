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
        self.cookies = ':nt_r=1; nt_r_ov=1; optimiza=58097b48ca664516; PHPSESSID=8oqp4mumkv6e9cm8flrvnnrum6; USERINFO=7iI5hYLyYCQ1dfpJJjlRdjlH31c%2F7lHba4XCdMq3q7t2bYffDQ6vht24KPy6U1DsvN6vQTE6lLg%3D; ASOD=6yLTg9MBT4AzroLDpiocG6U5; Hm_lvt_0bcb16196dddadaf61c121323a9ec0b6=1477016299,1477018483,1477018494,1477020566; Hm_lpvt_0bcb16196dddadaf61c121323a9ec0b6=1477146502'
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
                href.append(appCol.a['href'])
        return href

    def getAppId(self, detailURL):
        app_id = re.findall(re.compile('appid/(.*?)/country'), detailURL)
        return app_id[0]

    # 获得店铺页面html
    def getDetailPage(self, items, appID):
        try:

            appInfoURL = "http://aso100.com" + "/app/" + items + "/appid/" + appID + "/country/cn"
            request = urllib2.Request(appInfoURL, headers=self.headers)
            response = urllib2.urlopen(request)
            detailPage = response.read()
            detailPageCode = re.sub(r'<br[ ]?/?>', '\n', detailPage)
            return detailPageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

    # 获得app标题
    def getAppTitle(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        return soup.find("div", class_="appinfo-body").h3.getText()

    # 获得App版本信息
    def getAppVersion(self, page):

        soup = BeautifulSoup(page, 'html.parser')
        appVersionList = []
        # 更新日期，版本号
        tag = ["更新日期", "版本"]
        table = soup.find("table", class_="base-info base-area")
        infoTags = table.find_all("tr")
        for infoTag in infoTags:
            if str(infoTag.find("td").getText()) in tag:
                appVersionList.append(infoTag.find_all("td")[1].getText())
            else:
                continue
        return appVersionList

    # 获得App版本记录
    def getAppVersionRecord(self, page):
        #版本，更新日期，历史标题，更新说明
        soup = BeautifulSoup(page, 'html.parser')
        appVersionRecordList = []
        versionTr = soup.find("table", class_="table table-border version") \
            .find_all("tr")

        for versionTd in versionTr:
            try:

                appVersionRecord = []
                td = versionTd.find_all("td")
                appVersionRecord.append(td[0].getText())
                appVersionRecord.append(td[1].getText())
                appVersionRecord.append(td[2].getText())
                appVersionRecord.append(td[3].getText())
                appVersionRecordList.append(appVersionRecord)
            except IndexError, e:
                continue
        return appVersionRecordList
        # for i in range(0, len(appVersionRecordList)):
        #     appVersionDict[i] = appVersionRecordList[i]
        #     appVersionDict_json = json.dumps(appVersionDict, indent=1)
        # return appVersionDict_json

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

    # 获得时间范围
    def getTimeRange2(self):
        timeRange = {}
        sCurrentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        currentTime = datetime.datetime.strptime(sCurrentTime, "%Y-%m-%d %H:%M:%S")
        lastYearTime = currentTime - datetime.timedelta(days=365)
        sLastYearTime = lastYearTime.strftime("%Y-%m-%d %H:%M:%S")
        timeRange['currentTime'] = sCurrentTime
        timeRange['lastYearTime'] = sLastYearTime
        return timeRange

    # 获得APP排名
    def getAppRank(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find("table", class_="table no-hover rank table-border")
        appRank = []
        totalRank = table.find("td", class_="total").div.getText()
        classRank = table.find("td", class_="class").div.getText()
        appRank.append(totalRank)
        appRank.append(classRank)
        return appRank

    def downLoadFiles(self, frontURL, appID, behindURL):
        fileURL = self.siteURL + frontURL + appID + behindURL
        webbrowser.open(fileURL, new=0)

    def downLoadRank(self, appID, page):
        # 实时排名
        # /app/rankExport/appid/554499054/device/iphone/country/cn/
        # brand/all/sdate/2016-10-21 00:00:00/edate/2016-10-21 15:46:37
        frontURL = "/app/rankExport/appid/"
        behindURL = "/device/iphone/country/cn/brand/all/sdate/" + self.getTimeRange2()['lastYearTime'] \
                    + "/edate/" + self.getTimeRange2()['currentTime']
        self.downLoadFiles(frontURL, appID, behindURL)

    def downLoadComment(self, appID, page):
        # 评论详情
        # /app/commentListExport/appid/554499054/kdate/
        # 2016-10-14/ydate/2016-10-21/country/cn
        frontURL = "/app/commentListExport/appid/"
        behindURL = "kdate" + self.getTimeRange()['lastYearTime'] \
                    + "/ydate/" + self.getTimeRange()['currentTime'] \
                    + "/country/cn"
        self.downLoadFiles(frontURL, appID, behindURL)

    def downLoadKeyWord(self, appID, page):
        # 关键词
        # /app/keywordExport/appid/554499054/device/iphone/
        # country/cn/genre/36/ydate/2016-8-20/kdate/2016-9-21
        frontURL = "/app/keywordExport/appid/"
        behindURL = "/device/iphone/country/cn/genre/36/ydate/" + self.getTimeRange()['lastYearTime'] \
                    + "kdate/" + self.getTimeRange()['currentTime']
        self.downLoadFiles(frontURL, appID, behindURL)

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
        print "抓取中..."
        a = 0
        appList = []
        cur.execute("SELECT DISTINCT app_id FROM information ")
        results = cur.fetchall()
        result = list(results)
        for r in result:
            appList.append(int(r[0]))


        for i in appList:
            cur.execute("SELECT id FROM version WHERE app_id= " + str(i) + "")
            results = cur.fetchone()

            if results is not None:
                print "已存在"
                continue
            else:
                try:
                    appID = i
                    versionPage = self.getDetailPage("version",str(appID))
                    versionRecord = self.getAppVersionRecord(versionPage)


                    for j in range(0,60):
                        try:
                            versionDict = {}.fromkeys(
                                ('app_id', 'version', 'update_time', 'update_description', 'historytitle'))
                            versionDict['app_id'] = appID
                            versionDict['version'] = versionRecord[j][0]
                            versionDict['update_time'] = versionRecord[j][1]
                            versionDict['update_description'] = str(versionRecord[j][3]).replace("\n","")
                            versionDict['historytitle'] = str(versionRecord[j][2]).replace("\n","").replace("更多...","")

                            try:
                                cur.execute("INSERT INTO version(app_id,version,update_time,update_description,historytitle) \
                                                   VALUES     (%d     , '%s' ,'%s'       ,'%s'       ,'%s'  );" % \
                                        (versionDict['app_id'],versionDict['version'],versionDict['update_time'],versionDict['update_description']\
                                        ,versionDict['historytitle']))

                                conn.commit()
                            except:
                                continue
                        except IndexError ,e:
                            continue
                        print "数据+1"

                except AttributeError, e:
                    a += 1
                    print "抓取失败"
                    continue

        cur.close()
        conn.close()
        # print "抓取完成，共" + str(a) + "条记录"

aso = ASO100()
aso.start()
# url = "http://aso100.com/rank/index/device/iphone/country/cn/brand/free/genre/6003/date/2016-10-20"
# page = aso.getPage(url)
# hrefs = aso.getHref(page)
# for href in hrefs:
#     appID = aso.getAppId(href)
#     versionPage = aso.getDetailPage("version",appID)
#     print aso.getAppVersionRecord(versionPage)




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
