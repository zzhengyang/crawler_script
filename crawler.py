#coding:utf-8
import re
import urllib2
from bs4 import  BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


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
            page = response.read()
            pageCode = re.sub(r'<br[ ]?/?>', '\n', page)
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
            detailPage = response.read()
            detailPageCode = re.sub(r'<br[ ]?/?>', '\n', detailPage)
            return detailPageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

    #获得项目列表
    def getProject(self):
        page = self.getPage()
        soup = BeautifulSoup(page, 'html.parser')
        projectName = []
        projectId = {}
        projects = soup.find("div", class_="anchor-nav").stripped_strings
        for project in projects:
            projectName.append(project)
        for i in range(len(projectName)):
            projectId[i] = projectName[i]
        return projectId

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
            commentContent.append(item.find('img').get('src'))  #commentContent.append(item.find('div',class_="info").img.get('src'))暂时存在分界线不显示BUG
        return  commentContent


    #抓取游记链接
    def getTravel(self,page):
        soup = BeautifulSoup(page, 'html.parser')
        items = soup.find_all("li", class_="post-item clearfix")
        travelHref = []
        for item in items:
            travelHref.append(item.find('a').get('href'))
        return travelHref

    #判断是否存在信息列表
    def hasAttr(self,page,list):
        soup = BeautifulSoup(page, 'html.parser')
        col = soup.find("div", class_="col-main").find("div", class_="bd")
        str_col = str(col)
        if list in str_col:
            return True
        else:
            return False

    #抓取店铺信息
    def getShopInfo(self,page):
            shopInfoList = ['brief','localName','location', 'telephone', 'website', 'ticket', 'openTime','shopName','shopScore']
            infoItem = ['简介', '英文名称', '地址', '电话', '网址', '门票', '开放时间','名字','星评']
            soup = BeautifulSoup(page, 'html.parser')
            shopName = soup.find("div", class_="wrapper").h1.string
            shopScore = soup.find("div", class_="col-main").span.em.string

            for i in range(6):
                if self.hasAttr(page, infoItem[i]):
                        pattern_shopinfo = re.compile(
                            '<div class="col-main.*?<div class="bd">.*?'+ infoItem[i] +'</h3>.*?>(.*?)</p>', re.S)
                        shopInfos = re.findall(pattern_shopinfo, page)
                        for shopInfo in shopInfos:
                            shopInfoList[i] = shopInfo
                else:
                        continue

                shopInfoList[7] = shopName
                shopInfoList[8] = shopScore
            return shopInfoList



    #获取景点照片
    def getImage(self,page):
        soup = BeautifulSoup(page , 'html.parser')
        items = soup.find_all("div",class_="wrapper")

        for i in items:
            print i


    def startjob(self):
        f = open(r'e:/crawler.txt','w')
        f.truncate()
        shopProjects = self.getProject()
        for i in shopProjects.keys():
            f.write(str(i) + str(shopProjects[i]) + '\n')
        shopHrefList = self.getShopHref()
        for shopHref in shopHrefList:
            try:
                page = self.getDetailPage(shopHref)
                shopInfos = self.getShopInfo(page)
                for shopInfo in shopInfos:
                    f.write(str(shopInfo) + '\n')
                comments = self.getComment(page)
                for comment in comments:
                    f.write(str(comment) + '\n')
                travels = self.getTravel(page)
                for travel in travels:
                    f.write(str(travel) + '\n')
                f.write("======================================================================================================================" + '\n')
            except AttributeError, e:
                continue


        f.close()





mfw = MFW('普吉岛')
mfw.startjob()