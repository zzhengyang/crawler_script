# coding:utf-8
import re
import time
import traceback
from urllib import quote
import urllib2
import MySQLdb
from bs4 import BeautifulSoup
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class TA_CN:
    def __init__(self):
        self.siteURL = 'http://www.bangkok.com/cn'
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.items = ['开放时间','位置','电话']

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
    def getInfoItem(self, page):
        # page = self.getPage(url)
        soup = BeautifulSoup(page, 'html.parser')
        href = []
        items = soup.find_all("div", class_="top10_item_wrapper")
        return items

    def getHref(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        href = []
        items = soup.find_all("div", class_="top10_item_wrapper")
        # items = soup.find_all("div",class_="property_title")
        for item in items:
            href.append(item.a['href'])
        return href

    def getShopId(self, detailURL):
        shop_id = re.sub(r'.*?-d|-Revi.*', '', detailURL)
        return shop_id

    # 获得店铺页面html
    def getDetailPage(self, detailURL):
        try:

            shopURL = "http://www.tripadvisor.cn" + str(detailURL)
            request = urllib2.Request(shopURL, headers=self.headers)
            response = urllib2.urlopen(request)
            detailPage = response.read()
            detailPageCode = re.sub(r'<br[ ]?/?>', '\n', detailPage)
            return detailPageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None



    # 获得图片链接
    def getImaHref(self, page):
        imaHref = []
        soup = BeautifulSoup(page, 'html.parser')
        pictureList = soup.find_all("div", class_="content_listing_large")
        for pictureItem in pictureList:
            try:
                imaHref.append(str(pictureItem.img['data-src']))
            except:
                continue
        return imaHref

    # 获得店铺信息
    def getInfo(self, detailpage):

        shopInfoList = []
        #
        # # 店名，bio,描述，开放时间，位置,电话
        soup = BeautifulSoup(detailpage,'html.parser')
        tag = soup.find("div",class_="page_intro_body")
        try:
            shopName = tag.find("h1").getText()
        except AttributeError ,e:
            shopName = ''
        shopInfoList.append(shopName)

        try:
            shopBio = tag.find("h2").getText()
        except AttributeError ,e:
            shopBio = ''
        shopInfoList.append(shopBio)

        try:
            shopDescription = tag.find("p").getText()
        except AttributeError, e:
            shopDescription = ''
        shopInfoList.append(shopDescription)

        try:
            shopInfoTag = soup.find("ul",class_="listing_detail").find_all("li")
            for i in shopInfoTag:
                if str(i.find("strong").getText()) in self.items:
                    shopInfoList.append(str(i.getText()))
                else:
                    shopInfoList.append("")
        except AttributeError ,e:
            print "e"
        return shopInfoList


    # 获得店铺坐标
    def getLocation(self, page):
        location = []
        lat = re.findall(re.compile('lat: (.*?),'), page)
        location.append(lat[0])
        lng = re.findall(re.compile('lng: (.*?),'), page)
        location.append(lng[0])
        return location





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
        # try:
        url = "http://www.bangkok.com/cn/nightlife/top10-rooftop-bars.htm"
        page = self.getPage(url)
        hrefs= self.getHref(page)
        for href in hrefs:
            photos = []
            detailPage = self.getPage(href)
            shopInfoList = self.getInfo(detailPage)
            try:
                Infodict = {}.fromkeys(
                    ('city_id', 'bio', 'category_id', 'name', 'office_hours', 'lat', 'lng', \
                     'avgprice', 'address', 'phone', 'description', 'coordinate', 'photo_urls',
                     'content_image_url', 'ratings', 'ranking', 'shop_tag'))
                # # 店名，bio,描述，开放时间，位置,电话
                Infodict['city_id'] = 1
                Infodict['category_id'] = 4
                Infodict['name'] = shopInfoList[0]
                Infodict['office_hours'] = shopInfoList[3]
                Infodict['address'] = shopInfoList[4]
                Infodict['shop_id'] = 0
                shop_ima = {}
                photos =self.getImaHref(detailPage)
                for i in range(0, len(photos)):
                    shop_ima[i] = photos[i]
                    shop_ima_json = json.dumps(shop_ima, indent=1)

                #     try:
                #         Infodict['lat'] = float(location[0])
                #         Infodict['lng'] = float(location[1])
                #     except IndexError, e:
                Infodict['lat'] = float(0)
                Infodict['lng'] = float(0)
                Infodict['ratings'] = float(5)
                Infodict['bio'] = shopInfoList[1]
                Infodict['ranking'] = ''
                Infodict['avgprice'] = int(0)
                Infodict['shop_tag'] = ''
                Infodict['description'] = shopInfoList[2]
                Infodict['phone'] = shopInfoList[5]
                Infodict['photo_urls'] = str(shop_ima_json)
                try:
                    Infodict['content_image_url'] = str(photos[0])
                except IndexError, e:
                    Infodict['content_image_url'] = str('')


                try:
                    cur.execute("INSERT INTO merchants_bangkok(shop_id,name,category_id,coordinate,                 ratings,phone,city_id,avgprice,office_hours,address,bio,      description,photo_urls,content_image_url,ranking,shop_tag) \
                                                                                                    VALUES (%d,    '%s',%d,         ST_POINTFROMTEXT('POINT(%f %f)'),%.1f,    '%s', %d,     %f,      '%s',        '%s',   '%s',      '%s'   , '%s'    ,   '%s','%s','%s');" % \
                                (Infodict['shop_id'], Infodict['name'], Infodict['category_id'],
                                 Infodict['lng'], Infodict['lat'], Infodict['ratings'],
                                 Infodict['phone'],
                                 Infodict['city_id'], Infodict['avgprice'], Infodict['office_hours'],
                                 Infodict['address'], Infodict['bio'], Infodict['description'],
                                 Infodict['photo_urls'], Infodict['content_image_url'],
                                 Infodict['ranking'], Infodict['shop_tag']))
                    conn.commit()
                except:
                    print 'traceback.format_exc():\n%s' % traceback.format_exc()
                    # print "error"
                    continue
                a += 1
                print "抓取成功第" + str(a) + "条"


    #
    #
    #
    #
            except Exception, e:
                a += 1
                print 'traceback.format_exc():\n%s' % traceback.format_exc()
                # print "抓取失败"
                continue
    #
    # # except TypeError, e:
    # #     print "override"
    #
    #
    #
        cur.close()
        conn.close()
        print "抓取完成，共" + str(a) + "条记录"


ta_cn = TA_CN()

ta_cn.start()
# dzdp.getShopId('http://www.tripadvisor.cn/Search?geo=293917&pid=3826&q=按摩#&o=30&ssrc=a&dist=50km')
# url = "http://www.bangkok.com/cn/nightlife/top10-bars.htm"
# url = "file:///Users/Zyang/Movies/tripAdvisor_cn/geo=293916&pid=3826&q=spa%23&o=0.html"
# page = ta_cn.getPage(url)
# items = ta_cn.getInfoItem(page)
# for item in items:
#     print ta_cn.getInfo(item)[0]
# commentList = ta_cn.getComment(page)
# for i in commentList:
#     try:
#         z = i.find(name="div",attrs={"class","username mo"}).getText().replace("\n","")
#         print z
#     except:
#         continue
