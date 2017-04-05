#coding:utf-8
import re
import urllib2
from bs4 import  BeautifulSoup
import  json
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

    #获得美食单页店铺链接
    def getFoodHref(self,pageid):
        url = "/group/s.php?q="+self.city+"&p=" +str(pageid)+ "&t=cate&kt=1"
        page = self.getDetailPage(url)
        soup = BeautifulSoup(page,'html.parser')
        FoodHref = []
        FoodLists =  soup.find(name="div",attrs={'data-category':'poi'}).ul
        FoodHrefList = FoodLists.find_all("h3")
        for FoodHrefs in FoodHrefList:
            FoodWebsite = FoodHrefs.a['href']
            FoodHrefShort = str(FoodWebsite).replace('http://www.mafengwo.cn','')
            FoodHref.append(FoodHrefShort)
        return FoodHref

    def getHotelHref(self, pageid):
        url = "/group/s.php?q=" + self.city + "&p=" + str(pageid) + "&t=hotel&kt=1"
        page = self.getDetailPage(url)
        soup = BeautifulSoup(page, 'html.parser')
        hotelHref = []
        hotelHrefLists = soup.find_all("div",class_="hot-about clearfix _j_hotel")
        for hotelHrefList in hotelHrefLists:
            hotelWebsite= hotelHrefList.a['href']
            hotelHrefShort = str(hotelWebsite).replace('http://www.mafengwo.cn', '')
            hotelHref.append(hotelHrefShort)
        return hotelHref

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
            commentImas = item.find_all(name='img',attrs={'height':re.compile('.*?')})  #file'+'^((?!gif).)*$')}))  commentContent.append(item.find('div',class_="info").img.get('src'))暂时存在分界线不显示BUG
            for commentIma in commentImas:
                commentContent.append(commentIma.get('src'))
        return  commentContent

    #抓取酒店评论
    def getHotelComment(self,page):
        soup = BeautifulSoup(page , 'html.parser')
        list = soup.find("div", class_="hotel-comment")
        commentList = list.find_all("div",class_="comm-item _j_comment_item")
        #hotelCommentContent = []
        for item in commentList:
            print item.find("a",class_="txt").getText()
            #for i in hotelCommentContent:
                #print i

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

            for i in range(0,6):
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

    #抓取保存酒店数据
    def saveHotel(self):
        #f = open(r'e:/crawlerFood.txt','w')
        #f.truncate()
        a=0
        for i in range(51):
            try:
                hotelHrefList = self.getHotelHref(i)
                for hotelHref in hotelHrefList:
                    page = self.getDetailPage(hotelHref)
                    print page
                    #self.getHotelComment(page)
                    '''
                    f.write(str(shopInfo) + '\n')
                    comments = self.getComment(page)
                    for comment in comments:
                        f.write(str(comment) + '\n')
                    travels = self.getTravel(page)
                    for travel in travels:
                        f.write(str(travel) + '\n')
                    f.write("================================================================================="+"\n")
                    '''
            except AttributeError, e:
                continue
        #f.close()
        print "抓取完成"+"共"+str(a)+"条"

    #抓取保存餐厅数据
    def saveFood(self):
        #f = open(r'data/Food.txt','w')
        a=0
        for i in range(51):

            try:
                foodHrefList = self.getFoodHref(i)
                for foodHref in foodHrefList:
                    page = self.getDetailPage(foodHref)
                    dict = {}.fromkeys(('description','enname','location','telephone','website','ticket','opentime','name','rate'))
                    shopInfos = self.getShopInfo(page)
                    dict['description'] = shopInfos[0]
                    dict['enname'] = shopInfos[1]
                    dict['location'] = shopInfos[2]
                    dict['telephone'] = shopInfos[3]
                    dict['website'] = shopInfos[4]
                    dict['ticket'] = shopInfos[5]
                    dict['opentime'] = shopInfos[6]
                    dict['name'] = shopInfos[7]
                    dict['rate'] = shopInfos[8]
                    print json.dumps(dict,indent=1).decode("unicode_escape")
                    print ("=================================================================================" + "\n")
                    '''
                    shopInfos = self.getShopInfo(page)
                    for shopInfo in shopInfos:
                        f.write(str(shopInfo) + '\n')
                    comments = self.getComment(page)
                    for comment in comments:
                        f.write(str(comment) + '\n')
                    travels = self.getTravel(page)
                    for travel in travels:
                        f.write(str(travel) + '\n')
                    a += 1
                    f.write("================================================================================="+"\n")
            '''
            except AttributeError, e:
                continue
        #f.close()
        print "抓取完成"+"共"+str(a)+"条"

    #抓取保存娱乐信息
    def saveIntertainment(self):
        f = open(r'int.txt','a')
        f.write('\n城市:' + self.city + '\n\n\n')
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
        print "抓取完成"





mfw = MFW('曼谷')
mfw.saveFood()