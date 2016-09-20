#coding:utf-8

import urllib2
from bs4 import  BeautifulSoup

class MFW:

    def __init__(self,city):
        self.siteURL = 'http://www.mafengwo.cn'
        self.city = city
        self.cityDict = {'曼谷': '11045_518', '清迈': '15284_179', '普吉岛': '11047_858', '苏梅': '14210_686', '芭堤雅': '11046_940'}
        self.id = self.cityDict[self.city]
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
        self.headers = { 'User-Agent' :self.user_agent}

    #获得页面HTML
    def getPage(self):
        try:
            url = self.siteURL+"/baike/"+str(self.id)+".html"
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

    #获得下级WEB页面HTML
    def getDetailPage(self,detailURL):
        try:
            shopURL = "http://www.mafengwo.cn" + detailURL
            response = urllib2.urlopen(shopURL)
            detailPageCode = response.read().decode('utf-8')
            return detailPageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

    #获得项目列表
    def getProject(self):
        page = self.getPage()
        soup = BeautifulSoup(page , 'html.parser')
        projectName = []
        projects = soup.find("div", class_="anchor-nav").stripped_strings
        for project in projects:
            projectName.append(project)
        return projectName

    #获得店铺链接列表
    def getShopHref(self):
        page = self.getPage()
        soup = BeautifulSoup(page , 'html.parser')
        list = soup.find_all("div", class_="poi-card clearfix")
        shopHref = []
        for items in list:
            shopitem = items.find_all("div", class_="item")
            for item in shopitem:
                 shopHref.append(item.a['href'])
        return shopHref


    #抓取评论内容
    def getComment(self,page):
        soup = BeautifulSoup(page , 'html.parser')
        list = soup.find("div", class_="_j_commentlist")
        commentList = list.find_all("div", class_="comment-item")
        commentContent = []
        for item in commentList:
            commentContent.append(item.find('p').string)
        return  commentContent


    #抓取游记链接
    def getTravel(self,page):
        soup = BeautifulSoup(page, 'html.parser')
        items = soup.find_all("li", class_="post-item clearfix")
        travelHref = []
        for item in items:
            travelHref.append(item.find('a').get('href'))
        return travelHref

    #抓取店铺信息
    def getShopInfo(self,page):

        soup = BeautifulSoup(page , 'html.parser')
        shopName = soup.find("div", class_="wrapper").h1.string
        shopScore = soup.find("div", class_="col-main").span.em.string
        shopInfo = []
        shopInfo.append(shopName)
        shopInfo.append(shopScore)
        items = soup.find_all("div", class_="bd")
        for item in items:
            list = item.find_all('p')
            for tag in  list:
                shopInfo.append(tag.getText())
        return shopInfo

    #获取景点照片
    def getImage(self,page):
        soup = BeautifulSoup(page , 'html.parser')
        items = soup.find_all("div",class_="wrapper")

        for i in items:
            print i


    def startjob(self):

         shopHrefList = self.getShopHref()
         for shopHref in shopHrefList:
            page = self.getDetailPage(shopHref)
            shopInfos =self.getShopInfo(page)
            for shopInfo in shopInfos:
                print shopInfo
            comments = self.getComment(page)
            for comment in comments:
                print comment
            travels = self.getTravel(page)
            for travel in travels:
                print travel
            print "------------------------------------------------------"



mfw = MFW('普吉岛')
mfw.startjob()