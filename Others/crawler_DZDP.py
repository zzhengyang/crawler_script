#coding:utf-8
import re
import time
from urllib import quote
import urllib2
import MySQLdb
from bs4 import  BeautifulSoup
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class DZDP:
    def __init__(self):
        self.siteURL = 'http://www.dianping.com'
        self.category = {1:'按摩',2:'夜店',3:'泰拳',4:'人妖表演',5:'酒吧'}
        self.city = {1:'bangkok',2:'phuket',3:'pattaya',4:'chiangmai'}
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
    #获得主页面html
    def getPage(self,url):
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
        items = soup.find("div",id="searchList").find_all("li",class_="shopname")
        for item in items:
            href.append(item.a['href'])
        return href

    def getShopId(self,detailURL):
        shop_id = detailURL.replace('/shop/','')
        return shop_id




    #获得店铺页面html
    def getDetailPage(self,detailURL):
        try:

            shopURL = "http://www.dianping.com" + str(detailURL)
            request = urllib2.Request(shopURL, headers=self.headers)
            response = urllib2.urlopen(request)
            detailPage = response.read()
            detailPageCode = re.sub(r'<br[ ]?/?>', '\n', detailPage)
            return detailPageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

    #获得评论页面html
    def getCommentPage(self,detailURL,pageid):
        try:
            shopURL = "http://www.dianping.com" + str(detailURL) + '/review_all?pageno='+str(pageid)
            request = urllib2.Request(shopURL, headers=self.headers)
            response = urllib2.urlopen(request)
            commentPage = response.read()
            commentPageCode = re.sub(r'<br[ ]?/?>', '\n', commentPage)
            return commentPageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None



    #获得店铺评论图片
    def getCommentIma(self,page):
        commentImaHref = []
        soup = BeautifulSoup(page,'html.parser')
        commentList = soup.find("div",class_="comment-list")
        commentItems = commentList.find_all(name="li", attrs={"data-id":re.compile('^\d*$')})
        for commentItem in commentItems:
            try:
                commentImaHref.append(commentItem.find("div",class_="shop-photo").ul.li.a.img.get('src'))
            except AttributeError,e:
                continue
        return commentImaHref

    #获得店铺评论
    def getComment(self,page):
        comment = []
        soup = BeautifulSoup(page,'html.parser')
        commentList = soup.find("div",class_="comment-list").find_all(name="li",attrs={"data-id":re.compile('^\d*$')})
        for commentItem in commentList:
            comment.append(commentItem.find("div",class_="J_brief-cont").string.replace(' ','').replace('\n',''))
        return comment




    #获得店铺图片页面
    def getImaPage(self, detailURL):
        try:
            shopURL = "http://www.dianping.com" + str(detailURL) + '/photos'
            request = urllib2.Request(shopURL, headers=self.headers)
            response = urllib2.urlopen(request)
            imaPage = response.read()
            imaPageCode = re.sub(r'<br[ ]?/?>', '\n', imaPage)
            return imaPageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None


    #获得图片链接
    def getImaHref(self,page):
        imaHref = []
        soup = BeautifulSoup(page, 'html.parser')
        pictureList = soup.find("div",class_="picture-list").find_all("li",class_="J_list")
        for pictureItem in pictureList:
            imaHref.append(pictureItem.a['href'])
        return imaHref

    #获得图片
    def getIma(self,page):
        soup = BeautifulSoup(page,'html.parser')
        Ima = soup.find("div",class_="pic-wrap").img['src']
        return Ima

    #获得店铺信息
    def getInfo(self,page):

        soup = BeautifulSoup(page,'html.parser')
        shopInfoList = []
        #店名，地址，电话，营业时间
        shopNameTag = soup.find("div",class_="main")
        shopInfoList.append(shopNameTag.h1.stripped_strings.next())
        shopInfoList.append(shopNameTag.find("div", class_="expand-info address").find("span", class_="item").string)
        try:
            shopInfoList.append(shopNameTag.find("p", class_="expand-info tel").find("span", class_="item").string)
        except AttributeError, e:
            shopInfoList.append('Telephone')
        shopInfoList.append(shopNameTag.find("div", class_="other J-other ").find("span", class_="item").string)
        return shopInfoList

    #获得店铺坐标
    def getLocation(self,page):
        location = []
        lat = re.findall(re.compile(r'lat:(.*?)}'), page)
        for lats in lat:
            location.append(lats)
        lng = re.findall(re.compile(r'lng:(.*?),'), page)
        for lngs in lng:
            location.append(lngs)
        return location

    #店铺评分
    def getRatings(self,page):

        rating = re.findall(re.compile(r'mid-str(.*?)">'), page)
        return rating

    #获得店铺人均消费
    def getAvgPrice(self,page):

        avgPrices = re.findall(re.compile(r'class="item">人均：(.*?)</'),page)
        if avgPrices[0]=="-":
            avgPrice = '0'
        else:
            avgPrice = avgPrices[0].replace("元","")
        return avgPrice

    # 获得苏梅店铺页面链接
    def getSumeiPage(self):
        try:
            #http: // www.dianping.com / search / keyword / 2346 / 0_按摩 / p2
            shopURL ="http://www.dianping.com/search/keyword/2346/0_"+ str(self.item) +"/p" + str()
            request = urllib2.Request(shopURL, headers=self.headers)
            response = urllib2.urlopen(request)
            commentPage = response.read()
            commentPageCode = re.sub(r'<br[ ]?/?>', '\n', commentPage)
            return commentPageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None




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
        for city_id in range(1,5):
            for category_id in range(1, 5):
                for pageNum in range(1, 51):
                    try:
                        url = self.siteURL + "/" + str(self.city[city_id]) + "/search/" + "p" + str(pageNum) + "_" + str(quote(self.category[category_id]))

                        hrefs = self.getHref(url)
                        for href in hrefs:

                            shop_id = self.getShopId(href)

                            cur.execute("SELECT * FROM merchants WHERE shop_id = " + shop_id + "")
                            results = cur.fetchone()

                            if results is not None:
                                print "已存在"
                                a += 1
                                continue
                            else:
                                try:

                                    Infodict = {}.fromkeys(
                                        ('city_id', 'bio', 'category_id', 'name', 'office_hours', 'lat', 'lng', \
                                         'avgprice', 'address', 'phone', 'description', 'coordinate', 'photo_urls',
                                         'content_image_url', 'ratings'))
                                    page = self.getDetailPage(href)
                                    time.sleep(1.5)
                                    shopInfos = self.getInfo(page)

                                    time.sleep(1.5)
                                    location = self.getLocation(page)
                                    time.sleep(1.5)
                                    imgpage = self.getImaPage(href)
                                    shop_ima = {}
                                    photohrefs = self.getImaHref(imgpage)
                                    photos = []
                                    for photohref in photohrefs:
                                        photopage = self.getDetailPage(photohref)
                                        photos.append(self.getIma(photopage))
                                    for i in range(0, len(photos)):

                                        shop_ima[i] = photos[i]
                                    shop_ima_json = json.dumps(shop_ima, indent=1)

                                    Infodict['shop_id'] = int(shop_id)
                                    Infodict['city_id'] = int(city_id)
                                    Infodict['category_id'] = int(category_id)
                                    Infodict['name'] = str(shopInfos[0])
                                    Infodict['office_hours'] = str(shopInfos[3]).replace('\n', '').replace(' ', '')
                                    try:
                                        Infodict['avgprice'] = float(self.getAvgPrice(page))
                                    except IndexError, e:
                                        Infodict['avgprice'] = float('0')
                                    Infodict['address'] = str(shopInfos[1]).replace('\n', '').replace(' ', '')
                                    Infodict['phone'] = str(shopInfos[2])
                                    try:
                                        Infodict['lat'] = float(location[0])
                                        Infodict['lng'] = float(location[1])
                                    except IndexError, e:
                                        continue
                                    Infodict['photo_urls'] = str(shop_ima_json)
                                    try:
                                        Infodict['ratings'] = float(float(self.getRatings(page)[0]) / 10)
                                    except ValueError, e:
                                        Infodict['ratings'] = float('0')
                                    Infodict['bio'] = ''
                                    Infodict['description'] = ''
                                    Infodict['content_image_url'] = str(photos[0])

                                    try:
                                        cur.execute("INSERT INTO merchants(shop_id,name,category_id,coordinate,                 ratings,phone,city_id,avgprice,office_hours,address,bio,      description,photo_urls,content_image_url) \
                                                                                     VALUES (%d,    '%s',%d,         ST_POINTFROMTEXT('POINT(%f %f)'),%f,    '%s', %d,     %f,      '%s',        '%s',   '%s',      '%s'   , '%s'    ,   '%s');" % \
                                                    (Infodict['shop_id'], Infodict['name'], Infodict['category_id'],
                                                     Infodict['lat'], Infodict['lng'], Infodict['ratings'],
                                                     Infodict['phone'], Infodict['city_id'], Infodict['avgprice'],
                                                     Infodict['office_hours'], Infodict['address'], Infodict['bio'],
                                                     Infodict['description'], Infodict['photo_urls'],
                                                     Infodict['content_image_url']))
                                        conn.commit()
                                    except:
                                        continue


                                    # for commentpagenum in range(3):
                                    #     Commentdict = {}.fromkeys(('shop_id','comment'))
                                    #     commentPage = self.getCommentPage(href, commentpagenum)
                                    #     for comment in  self.getComment(commentPage):
                                    #
                                    #         Commentdict['shop_id'] = Infodict['shop_id']
                                    #         Commentdict['comment'] = comment
                                    #
                                    #
                                    #                                             try:
                                    #     cur.execute("INSERT INTO merchants(shop_id,name,category_id,coordinate,                 ratings,phone,city_id,avgprice,office_hours,address,bio,      description,photo_urls,content_image_url) \
                                    #                                                  VALUES (%d,    '%s',%d,         ST_POINTFROMTEXT('POINT(%f %f)'),%f,    '%s', %d,     %f,      '%s',        '%s',   '%s',      '%s'   , '%s'    ,   '%s');" % \
                                    #                 (Infodict['shop_id'], Infodict['name'], Infodict['category_id'],
                                    #                  Infodict['lat'], Infodict['lng'], Infodict['ratings'],
                                    #                  Infodict['phone'], Infodict['city_id'], Infodict['avgprice'],
                                    #                  Infodict['office_hours'], Infodict['address'], Infodict['bio'],
                                    #                  Infodict['description'], Infodict['photo_urls'],
                                    #                  Infodict['content_image_url']))
                                    #     conn.commit()
                                    # except:
                                    #     continue


                                except AttributeError, e:
                                    continue
                                a += 1
                                print "抓取成功第" + str(a) + "条"

                    except AttributeError, e:
                        continue
        cur.close()
        conn.close()
        print "抓取完成，共" + str(a) + "条记录"







dzdp = DZDP()
dzdp.start()




