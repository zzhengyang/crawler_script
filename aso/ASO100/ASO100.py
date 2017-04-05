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
        self.item={'天气':'6001','工具':'6002','旅游':'6003','体育':'6004','社交':'6005','参考':'6006','效率':'6007'\
            ,'摄影与录像':'6008','新闻':'6009','导航':'6010','音乐':'6011','生活':'6012','健康健美':'6013','游戏':'6014'\
            ,'财务':'6015','娱乐':'6016','教育':'6017','图书':'6018','医疗':'6020','报刊杂志':'6021','商品指南':'6022',\
                   '美食佳饮':'6023','购物':'6024','贴纸':'6025'}
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
        soup = BeautifulSoup(page, 'html.parser')
        # appVersionDict = {}
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
        try:
            totalRank = table.find("td", class_="total").div.getText()
            appRank.append(totalRank)
        except AttributeError, e:
            appRank.append(0)
        try:
            classRank = table.find("td", class_="class").div.getText()
            appRank.append(classRank)
        except AttributeError,e:
            appRank.append(0)
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

    def start(self,item):

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
        for i in range(0, 365):
            queryDate = self.getTimeRange(i)['lastYearTime']
            # http://aso100.com/rank/index/device/iphone/country/cn/brand/free/genre/6003/date/2016-10-20
            url = "http://aso100.com/rank/index/device/iphone/country/cn/brand/free/genre/"+self.item[item]+"/date/" + queryDate
            page = self.getPage(url)
            hrefs = self.getHref(page)
            hrefList = [hrefs[i] for i in range(0, 100)]
            for href in hrefList:
                appID = self.getAppId(href)
                cur.execute("SELECT id FROM app_id WHERE query_date = '%s'  and app_id = '%d' " %(queryDate,int(appID)))
                results = cur.fetchone()
                if results is not None:
                    print "已存在"

                    continue
                else:
                    cur.execute("INSERT INTO app_id(app_id,category_id,category,query_date) \
                                            VALUES(%d,     %d          , '%s','%s')"%\
                                                (int(appID),int(self.item[item]),item,queryDate))
                    conn.commit()
                    a+=1
                    print "第"+str(a)+"条"
                    # try:
                    #     infoPage = self.getDetailPage("baseinfo", appID)
                    #     title = self.getAppTitle(infoPage)
                    #     version = self.getAppVersion(infoPage)[1]
                    #     latest_date = self.getAppVersion(infoPage)[0]
                    #
                    #     rankPage = self.getDetailPage("rank", appID)
                    #     rank = self.getAppRank(rankPage)
                    #     total_rank = rank[0]
                    #     class_rank = rank[1]
                    #
                    #     infoDict = {}.fromkeys(
                    #         ('app_id', 'name', 'latest_date', 'version', 'total_rank',
                    #          'class_rank', 'date'))
                    #     infoDict['app_id'] = int(appID)
                    #     infoDict['name'] = title
                    #     infoDict['latest_date'] = latest_date
                    #     infoDict['version'] = version
                    #     infoDict['total_rank'] = int(total_rank)
                    #     infoDict['class_rank'] = int(class_rank)
                    #     infoDict['date'] = queryDate
                    #
                    #     try:
                    #         cur.execute("INSERT INTO information(name,app_id,latest_date,version,total_rank,class_rank,query_date)\
                    #                                      VALUES('%s',%d    ,'%s'       ,'%s'   ,%d        ,%d        ,'%s');" % \
                    #                     (infoDict['name'], infoDict['app_id'], infoDict['latest_date'] \
                    #                          , infoDict['version'], infoDict['total_rank'], infoDict['class_rank'],
                    #                      queryDate))
                    #         conn.commit()
                    #
                    #
                    #     except:
                    #         a+=1
                    #         print "插入失败"
                    #         continue
                    #     a += 1
                    #     print "抓取成功第" + str(a) + "条"
                    #
                    #
                    #
                    #
                    # except AttributeError, e:
                    #     a += 1
                    #     print "抓取失败"
                    #     continue


        cur.close()
        conn.close()
        print "抓取完成，共" + str(a) + "条记录"

aso = ASO100()
aso.start("体育")
# url = "http://aso100.com/rank/index/device/iphone/country/cn/brand/free/genre/6003/date/2016-10-20"
# page = aso.getPage(url)
# hrefs = aso.getHref(page)
# for href in hrefs:
#     appID = aso.getAppId(href)





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
