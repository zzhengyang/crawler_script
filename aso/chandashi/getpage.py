#!/usr/bin/python
#coding:utf-8
import ast
import re
import urllib2

import MySQLdb
import datetime
import requests

import sys
import time
import xlrd
from tqdm import tqdm

reload(sys)
sys.setdefaultencoding('utf-8')

class Chan:
    def __init__(self):
        self.baseURL = 'https://www.chandashi.com'
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.username = '15988129425'
        self.password = 'zhengy1995'
        self.login_url = self.baseURL + '/user/login/appId/1089850733.html'

    def getPage(self, url):
        try:
            s = requests.Session()
            s.post(self.login_url, {'username': self.username, 'password': self.password }, headers=self.headers)
            page = s.get(url).text
            pageCode = re.sub(r'<br[ ]?/?>', '\n', page)
            return pageCode
        except:
        # except urllib2.URLError, e:
        #     if hasattr(e, "reason"):
        #         print e.reason
                return None



    def getKeyWordInfo(self, page, appID, appName):
        keyWordInfoList = re.findall(r'keywordData = (.*);', page)
        appKeywordList = []
        todayTime = datetime.datetime.now().strftime("%Y-%m-%d ")
        for i in eval(str(keyWordInfoList[0])):
            try:
                singleKeywordInfo = []
                keyword = i[0]
                rank = str(i[1]).split('|', 1)
                keywordRank = int(rank[0])
                keywordFloatRank = int(rank[1])
                keywordPriority = i[2]
                keywordSearchCount = i[3]
                queryDateStr = str(i[6]).split(' ', 1)[1]
                time = todayTime + queryDateStr
                queryDate = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
            except ValueError, e:
                continue

            singleKeywordInfo = [appID, appName, keyword, keywordRank, keywordFloatRank, keywordPriority, keywordSearchCount, queryDate]
            appKeywordList.append(singleKeywordInfo)

        return appKeywordList

    def excelAppIdReader(self):
        data = xlrd.open_workbook('./chan.xlsx')
        table = data.sheets()[0]
        appIdList = []
        nrows = table.nrows
        for i in range(nrows):
            appIdList.append([table.row_values(i)[0],table.row_values(i)[1]])
        return appIdList

    def excelAppKeywordReader(self):
        data = xlrd.open_workbook('./chan.xlsx')
        table = data.sheets()[0]
        nrows = table.nrows

        appKeywordDictList = []
        for i in range(nrows):
            appKeywordDict = {}

            appKeywordDict[int(table.row_values(i)[0])] = table.row_values(i)[2:]
            appKeywordDictList.append(appKeywordDict)
        return appKeywordDictList

    def catchFullKeyword(self):
        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            passwd='root',
            db='cq_aso',
            port=3306,
            charset="utf8"
        )
        cur = conn.cursor()
        cur.execute("TRUNCATE TABLE chan_aso")
        stm = 'INSERT INTO chan_aso(appId,appName,keyword,keyword_rank,keyword_float,keyword_priority,keyword_search_count,query_date) VALUES (%s,%s, %s,%s,%s,%s,%s,%s)'
        for appIdNameList in tqdm(self.excelAppIdReader()):
            page = self.getPage(
                self.baseURL + '/apps/keywordcover/appId/' + str(int(appIdNameList[0])) + '/country/cn.html')
            appKeywordList = self.getKeyWordInfo(page, int(appIdNameList[0]), str(appIdNameList[1]))
            cur.executemany(stm, appKeywordList)
            conn.commit()

        cur.close()
        conn.close()
        self.getPage(self.baseURL + '/update/app/appId/1089850733/country/cn.html')
        return True

    def getKeywordFromSQL(self):
        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            passwd='root',
            db='cq_aso',
            port=3306,
            charset="utf8"
        )
        cur = conn.cursor()
        # if chan.catchFullKeyword():
        for i in self.excelAppKeywordReader():
            for j in i.values()[0]:
                cur.execute(
                    "INSERT INTO chan_aso_keyword(appId,appName,keyword,keyword_rank,keyword_float,keyword_priority,keyword_search_count,query_date) SELECT appId,appName,keyword,keyword_rank,keyword_float,keyword_priority,keyword_search_count,query_date FROM chan_aso WHERE appId=%s AND keyword=%s",
                    (i.keys()[0], j))
                conn.commit()
        cur.close()
        conn.close()
        return True
def start():
    chan = Chan()
    while True:
        if chan.catchFullKeyword():
            print chan.getKeywordFromSQL()
            print time.ctime()
            time.sleep(30*60)
if __name__ == '__main__':
    start()