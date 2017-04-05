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


class TA_EN:
    def __init__(self):
        self.siteURL = 'http://www.tripadvisor.com'
        self.category = {1: 'spa', 2: quote('夜店'), 3: quote('夜宵'), 4: quote('酒吧'), 5: quote('表演')}
        self.city = {1: '293916', 2: '293920', 3: '293919', 4: '293917', 5: '293918'}  # 曼谷，普吉，芭堤雅，清迈，苏梅岛
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

    # 获得店铺页面链接
    def getHref(self, url):
        page = self.getPage(url)
        soup = BeautifulSoup(page, 'html.parser')
        href = []
        items = soup.find_all("h3",class_="title")
        # items = soup.find_all("div", class_="property_title")
        for item in items:
            href.append(item.a['href'])
        return href

    def getShopId(self, detailURL):
        shop_id = re.sub(r'.*?-d|-Revi.*', '', detailURL)
        return shop_id

    # 获得店铺页面html
    def getDetailPage(self, detailURL):
        try:

            shopURL = self.siteURL + str(detailURL)
            request = urllib2.Request(shopURL, headers=self.headers)
            response = urllib2.urlopen(request)
            detailPage = response.read()
            detailPageCode = re.sub(r'<br[ ]?/?>', '\n', detailPage)
            return detailPageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

    # 获得评论页面html
    def getCommentPage(self, detailURL, pageid):
        try:
            shopURL = "http://www.dianping.com" + str(detailURL) + '/review_all?pageno=' + str(pageid)
            request = urllib2.Request(shopURL, headers=self.headers)
            response = urllib2.urlopen(request)
            commentPage = response.read()
            commentPageCode = re.sub(r'<br[ ]?/?>', '\n', commentPage)
            return commentPageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

    # 获得店铺评论图片
    def getCommentIma(self, page):
        commentImaHref = []
        soup = BeautifulSoup(page, 'html.parser')
        commentList = soup.find("div", class_="comment-list")
        commentItems = commentList.find_all(name="li", attrs={"data-id": re.compile('^\d*$')})
        for commentItem in commentItems:
            try:
                commentImaHref.append(commentItem.find("div", class_="shop-photo").ul.li.a.img.get('src'))
            except AttributeError, e:
                continue
        return commentImaHref

    # 获得店铺评论
    def getComment(self, page):
        comment = []
        soup = BeautifulSoup(page, 'html.parser')
        commentList =soup.find_all(name="div", attrs={"class": re.compile('reviewSelector.*?'),"id":re.compile('review_.*?')})
        # for commentItem in commentList:
        #     comment.append(commentItem.string)
        return commentList

    # 获得店铺图片页面
    def getImaPage(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        photoPageURL = soup.find("div", class_="main_section photobar").a['href']
        photoPage = self.getDetailPage(photoPageURL)
        return photoPage

    # 获得图片链接
    def getImaHref(self, page):
        imaHref = []
        if page is None:
            return imaHref
        else:
            soup = BeautifulSoup(page, 'html.parser')
            pictureList = soup.find_all("div", class_="imgBx")
            for pictureItem in pictureList:
                imaHref.append(pictureItem.find('img').get('src'))
            return imaHref

    # 获得店铺信息
    def getInfo(self, page):

        soup = BeautifulSoup(page, 'html.parser')
        shopInfoList = []
        # 店名，地址，电话，营业时间，描述
        shopInfoList.append(soup.find("div", class_="warLocName").string)

        try:
            shopLocation1 = soup.find("span", class_="extended-address").string
            shopLocation2 = soup.find("span", class_="street-address").string
            shopLocation = shopLocation2 + '|' + shopLocation1
            shopInfoList.append(shopLocation)
        except AttributeError, e:
            shopInfoList.append("")

        try:
            shopInfoList.append(soup.find("div", class_="phoneNumber").string)
        except AttributeError, e:
            shopInfoList.append("")

        try:
            shopTimeList = []
            shopOfficeTimes = soup.find("div", id="HOUR_OVERLAY_CONTENTS").find_all("span")
            for shopTime in shopOfficeTimes:
                shopTimeList.append(shopTime.string.replace("\n", ""))
                shopOfficeTime = ''.join(shopTimeList)
            shopInfoList.append(shopOfficeTime)
        except:
            shopInfoList.append("")
        try:
            shopDesTag = soup.find("div", class_="listing_details").getText()
            shopInfoList.append(shopDesTag)
        except AttributeError, e:
            shopInfoList.append("")
        return shopInfoList

    # 获得店铺坐标
    def getLocation(self, page):
        location = []
        lat = re.findall(re.compile('lat: (.*?),'), page)
        location.append(lat[0])
        lng = re.findall(re.compile('lng: (.*?),'), page)
        location.append(lng[0])
        return location

    # 店铺评分
    def getRatings(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        try:
            rating = soup.find("div", class_="rs rating").img['content']
        except:
            rating = '0'
        return rating

    # 店铺标签
    def getShopTag(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        tag = soup.find("div", class_="heading_details").getText().replace("\n", "")
        return tag

    # 店铺排名
    def getRanking(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        ranking = soup.find("div", class_="slim_ranking").getText().replace('\n', '')
        return ranking

    # 获得店铺人均消费
    def getAvgPrice(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        avgPrices = soup.find("div", class_="offer_price_box").find("div", class_="display_price smaller").getText()
        avgPrice = str(avgPrices).replace("CN¥", "").replace("*", "")
        return avgPrice

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
        for city_id in range(1, 6):
            for category_id in range(1, 6):
                for pageNum in range(0, 300, 30):
                    try:
                        # url = "https://www.tripadvisor.com.tr/Attraction_Review-g293916-d496987-Reviews-Wat_Pho_Thai_Traditional_Massage_School-Bangkok.html"
                        url = "file:///Users/Zyang/Movies/tripadvisor_en/geo=" + str(
                            self.city[city_id]) + "&pid=3826&q=" \
                              + str(self.category[category_id]) + "%23&o=" + str(pageNum) + ".html"
                        hrefs = self.getHref(url)

                        for href in hrefs:
                            shop_id = self.getShopId(href)
                            # cur.execute("SELECT id FROM merchants_en WHERE shop_id=" + shop_id + "")
                            # results = cur.fetchone()
                            #
                            # if results is not None:
                            #     print "已存在"
                            #     a += 1
                            #     continue
                            # else:
                            try:
                                #
                                #         Infodict = {}.fromkeys(
                                #             ('city_id', 'bio', 'category_id', 'name', 'office_hours', 'lat', 'lng', \
                                #              'avgprice', 'address', 'phone', 'description', 'coordinate', 'photo_urls',
                                #              'content_image_url', 'ratings', 'ranking', 'shop_tag'))
                                #         page = self.getDetailPage(href)
                                #
                                #         shopInfos = self.getInfo(page)
                                #         time.sleep(1.5)
                                #         location = self.getLocation(page)
                                #         time.sleep(1.5)
                                #         imgpage = self.getImaPage(page)
                                #         shop_ima = {}
                                #         photos = self.getImaHref(imgpage)
                                #         for i in range(0, len(photos)):
                                #             shop_ima[i] = photos[i]
                                #         shop_ima_json = json.dumps(shop_ima, indent=1)
                                #
                                #         Infodict['ranking'] = str(self.getRanking(page))
                                #         Infodict['shop_tag'] = str(self.getShopTag(page))
                                #         Infodict['shop_id'] = int(shop_id)
                                #         Infodict['city_id'] = int(city_id)
                                #         Infodict['category_id'] = int(category_id)
                                #         Infodict['name'] = str(shopInfos[0]).replace("'", "")
                                #         Infodict['office_hours'] = str(shopInfos[3]).replace('\n', '').replace(' ', '')
                                #         try:
                                #             Infodict['avgprice'] = float(self.getAvgPrice(page))
                                #         except:
                                #             Infodict['avgprice'] = float('0')
                                #         Infodict['address'] = str(shopInfos[1]).replace('\n', '').replace(' ', '')
                                #         Infodict['phone'] = str(shopInfos[2]).replace("Phone Number: ", "")
                                #         try:
                                #             Infodict['lat'] = float(location[0])
                                #             Infodict['lng'] = float(location[1])
                                #         except IndexError, e:
                                #             Infodict['lat'] = float(0)
                                #             Infodict['lng'] = float(0)
                                #         Infodict['photo_urls'] = str(shop_ima_json)
                                #         Infodict['ratings'] = float(self.getRatings(page)[0])
                                #         Infodict['bio'] = ''
                                #         try:
                                #             Infodict['description'] = str(shopInfos[4]).replace('\n', '').replace("'", "")
                                #         except:
                                #             Infodict['description'] = str('')
                                #         try:
                                #             Infodict['content_image_url'] = str(photos[0])
                                #         except IndexError, e:
                                #             Infodict['content_image_url'] = str('')
                                #         print Infodict
                                #         try:
                                #             cur.execute("INSERT INTO merchants_en(shop_id,name,category_id,coordinate,                 ratings,phone,city_id,avgprice,office_hours,address,bio,      description,photo_urls,content_image_url,ranking,shop_tag) \
                                #                                                                                                                                                                                                     VALUES (%d,    '%s',%d,         ST_POINTFROMTEXT('POINT(%f %f)'),%.1f,    '%s', %d,     %f,      '%s',        '%s',   '%s',      '%s'   , '%s'    ,   '%s','%s','%s');" % \
                                #                         (Infodict['shop_id'], Infodict['name'], Infodict['category_id'],
                                #                          Infodict['lng'], Infodict['lat'], Infodict['ratings'],
                                #                          Infodict['phone'],
                                #                          Infodict['city_id'], Infodict['avgprice'],
                                #                          Infodict['office_hours'],
                                #                          Infodict['address'], Infodict['bio'], Infodict['description'],
                                #                          Infodict['photo_urls'], Infodict['content_image_url'],
                                #                          Infodict['ranking'], Infodict['shop_tag']))
                                #             conn.commit()
                                #
                                #         except:
                                #             print "error"
                                #             continue
                                #         a += 1
                                #         print "抓取成功第" + str(a) + "条"


                                page = self.getDetailPage(href)
                                Commentdict = {}.fromkeys(
                                    ('shop_id', 'merchant_id', 'created_by', 'author_name', 'content'))
                                # time.sleep(1.5)
                                commentList = self.getComment(page)
                                for commentItem in commentList:
                                    cur.execute("select id from merchants_en where shop_id = " + shop_id + ";")
                                    merchant_id = cur.fetchone()
                                    Commentdict['merchant_id'] = int(merchant_id[0])
                                    Commentdict['created_by'] = int('0')
                                    try:
                                        Commentdict['author_name'] = str(
                                            commentItem.find(name="div",attrs={"class", "username mo"}).getText()).replace("\n","")
                                    except AttributeError, e:
                                        continue
                                    # time.sleep(1.5)
                                    Commentdict['shop_id'] = int(shop_id)
                                    try:
                                        Commentdict['content'] = str(
                                            commentItem.find("p", class_="partial_entry").getText()).replace("\n", "")
                                    except AttributeError, e:
                                        continue

                                        # cur.execute("SELECT id FROM comments_en WHERE author_name='" + Commentdict[
                                        #     'author_name'] + "'")
                                        # results = cur.fetchone()
                                        #
                                        # if results is not None:
                                        #     print "已存在"
                                        #     continue
                                        # else:


                                    try:
                                        cur.execute("INSERT INTO comments_en(shop_id,merchant_id,created_by,author_name,content) \
                                                                                                                      VALUES (%d     , %d        ,%d        ,'%s'       ,'%s'  );" % \
                                                    (Commentdict['shop_id'], Commentdict['merchant_id'],
                                                     Commentdict['created_by'], Commentdict['author_name'],
                                                     Commentdict['content']))
                                        conn.commit()
                                    except:
                                        continue
                                    print "数据+1"





                            except AttributeError, e:
                                a += 1
                                print "抓取失败"
                                continue




                    except TypeError, e:
                        print "override"
                        continue

        cur.close()
        conn.close()
        print "抓取完成，共" + str(a) + "条记录"


ta_en = TA_EN()

ta_en.start()
# dzdp.getShopId('http://www.tripadvisor.cn/Search?geo=293917&pid=3826&q=按摩#&o=30&ssrc=a&dist=50km')
# url = "http://www.tripadvisor.cn/Restaurants-g293916-zfp8-Bangkok.html"
# url = "https://www.tripadvisor.com/Attraction_Review-g293916-d496987-Reviews-Wat_Pho_Thai_Traditional_Massage_School-Bangkok.html"
# page = ta_en.getPage(url)
# commentList =ta_en.getComment(page)
# for i in commentList:
#     # print str(i.find("p",class_="partial_entry").getText()).replace("\n","").replace("...More","")
#     print str(i.find(name="div",attrs={"class", "username mo"}).getText()).replace("\n","")
# imapage = dzdp.getImaPage(page)
# print dzdp.getImaHref(imapage)
