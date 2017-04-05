# coding:utf-8
import re
import time
from urllib import quote
import urllib2
import MySQLdb
from bs4 import BeautifulSoup
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class SIAM:
    def __init__(self):
        self.siteURL = 'https://www.siam2nite.com/en/'
        self.category = {1: 'concerts', 2: 'international-djs', 3: 'festivals', 4: 'pool-parties'}
        self.city = {1: '', 2: 'phuket/', 3: 'pattaya/', 4: 'chiangmai/', 5: 'kohsamui/'}  # 曼谷，普吉，芭堤雅，清迈，苏梅岛
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}


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

    # 获得活动链接
    def getHref(self, page):

        soup = BeautifulSoup(page, 'html.parser')
        href = []
        eventsList = soup.find("div",class_="small-12 medium-12 large-8 columns")
        events = eventsList.find_all(name="div", attrs={"class": re.compile('event-item event-item--main.*?')})
        # # items = soup.find_all("div",class_="property_title")
        for item in events:
            href.append(item.a['href'])
        return href


    # 获得活动页面
    def getDetailPage(self, detailURL):
        try:

            shopURL =str(detailURL)
            request = urllib2.Request(shopURL, headers=self.headers)
            response = urllib2.urlopen(request)
            detailPage = response.read()
            detailPageCode = re.sub(r'<br[ ]?/?>', '\n', detailPage)
            return detailPageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None



    # 获得活动信息
    def getInfo(self, page):

        soup = BeautifulSoup(page, 'html.parser')
        shopTag = []
        Infodict = {}.fromkeys(
                    ( 'name', 'date','hours' ,'lat', 'lng', 'title',\
                     'avgprice','description', 'phone', 'description', 'photo_url','shop_tag'))

        # 图片，标题，描述，店名，日期，时间，标签
        Infodict['photo_url'] = soup.find("div", class_=" ratio__425-160").img['src']  #图片

        Infodict['title']  = soup.find("h1",class_="event__title").string   #标题
        Infodict['description'] = soup.find("p", class_="event__description").string  #描述
        columns = soup.find("div", class_="row small-up-2 collapse").findAll("div", class_="columns")
        for column in columns:
            columnIcon = column.find("div",class_="event__meta-list-icon").i['class'][0]
            if columnIcon in 'icons8-map-marker':
                Infodict['name'] = column.find("div", class_="event__meta-list-text").string.replace('\n','').replace(' ','').replace('\t','')  #店名
                localHref = column.a['href'] # 坐标
                location = re.sub(r'^.*?q=','',localHref)
                Infodict['lat'] = re.findall(r'^(.*?),',location)[0]
                Infodict['lng'] = re.findall(r',(.*?)$',location)[0]
            elif columnIcon in 'icons8-cheap-2':
                try:
                    Infodict['avgprice'] = column.find("div",class_="event__meta-list-text event__meta-list-text--no-link").string.replace('\n','').replace('\t','')  #价格
                except:
                    Infodict['avgprice'] = 0
            elif columnIcon in 'icons8-calendar':
                try:
                    Infodict['date'] = column.find("div", class_="event__meta-list-text event__meta-list-text--no-link").string.replace('\n','').replace('\t','')  # 日期
                except:
                    Infodict['date'] = ''
            elif columnIcon in 'icons8-clock':
                try:
                    Infodict['hours'] = column.find("div", class_="event__meta-list-text event__meta-list-text--no-link").string  # 时间
                except:
                    Infodict['hours'] = ''
        raws = soup.find("div", class_="event__meta-list").findAll("div", class_="event__meta-list-item")
        for raw in raws:
            rawIcon = raw.find("div",class_="event__meta-list-icon").i['class'][0]
            if rawIcon in 'icons8-music-record':
                shopTags = raw.find("div",class_="event__meta-list-content").findAll("span")
                for i in shopTags:
                    shopTag.append(i.string.replace(';',''))
            Infodict['shop_tag'] = shopTag
        return Infodict



    def start(self):
        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            passwd='root',
            db='dtrip',
            port=3306,
            charset="utf8"
        )
        cur = conn.cursor()
        print "抓取中..."
        a = 0

        # 曼谷
        # for category_id in range(1, 5):
        # # for city_id in range(2,6):
        #             # print self.category[category_id] + "============\n"
        #             try:
        #                 url = self.siteURL + self.city[1] + 'events/' + self.category[category_id]
        #                 page = self.getPage(url)
        #                 eventList = self.getHref(page)
        #                 for i in eventList:
        #                     eventPage = self.getDetailPage(i)
        #                     result = self.getInfo(eventPage)
        #
        #                     cur.execute("insert into events_test(name,city_id,coordinate,                      category,photo_url,content,hold_date,hold_time,sponsor,status,shop_tag,avgprice) \
        #                                                     values(%s,  %s   ,ST_POINTFROMTEXT('POINT(%s %s)'),%s,      %s      ,%s      ,%s        ,%s        ,%s     ,%s,      %s  ,%s);" , \
        #                                 (result['title'], 1, float(result['lng']), float(result['lat']), 1, result['photo_url'],result['description'], result['date'], result['hours'], result['name'], 1,str(result['shop_tag']).replace("u'","").replace("'",""),result['avgprice']))
        #                     conn.commit()
        #                     # time.sleep(0.5)
        #                     print "+1"
        #
        #             except TypeError, e:
        #                 print "override"
        #                 continue

        #其他城市
        for city_id in range(2,6):
                        # print self.category[category_id] + "============\n"
                        try:
                            url = self.siteURL + self.city[city_id] + 'events/' #+ self.category[category_id]
                            page = self.getPage(url)
                            eventList = self.getHref(page)
                            for i in eventList:
                                eventPage = self.getDetailPage(i)
                                result = self.getInfo(eventPage)

                                cur.execute("insert into events_test(name,city_id,coordinate,                      category,photo_url,content,hold_date,hold_time,sponsor,status,shop_tag,avgprice) \
                                                                                    values(%s,  %s   ,ST_POINTFROMTEXT('POINT(%s %s)'),%s,      %s      ,%s      ,%s        ,%s        ,%s     ,%s,      %s  ,%s);", \
                                            (result['title'], city_id, float(result['lng']), float(result['lat']), 1,
                                             result['photo_url'], result['description'], result['date'],
                                             result['hours'], result['name'], 1,
                                             str(result['shop_tag']).replace("u'", "").replace("'", ""),
                                             result['avgprice']))
                                conn.commit()
                                # time.sleep(0.5)
                                print "+1"

                        except TypeError, e:
                            print "override"
                            continue


        #                 for href in hrefs:
        #                     shop_id = self.getShopId(href)
                            # cur.execute("SELECT id FROM comments_cn WHERE shop_id=" + shop_id + "")
                            # results = cur.fetchone()
                            #
                            # if results is not None:
                            #     print "已存在"
                            #     a += 1
                            #     continue
                            # else:


                    #         except AttributeError, e:
                    #                 a += 1
                    #                 print "抓取失败"
                    #                 continue
                    #
                    #
                    #
                    #
                    # except TypeError, e:
                    #     print "override"
                    #     continue

        cur.close()
        conn.close()
        print "抓取完成，共" + str(a) + "条记录"


siam = SIAM()
siam.start()
# page = siam.getPage(siam.siteURL+"events/concerts")
# eventList =  siam.getHref(page)
# for i in eventList:
#     eventPage = siam.getDetailPage(i)
#     siam.getInfo(eventPage)
# print eventList


