#coding:utf-8
import urllib
import re
import urllib2
import requests
from bs4 import  BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


'''class DZDP:
    def __init__(self,city):
        self.siteURL = 'http://www.dianping.com'
        self.city = city
        self.cityDict = {'曼谷': 'bangkok', '清迈': 'chiangmai', '普吉岛': 'phuket', '苏梅': 'samui',
                         '芭堤雅': 'pattaya'}

        self.cityName = self.cityDict[self.city]
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
        self.headers = {'User-Agent': self.user_agent}
    def getPage(self,pageNum):
        try:
            url = self.siteURL+"/"+str(self.cityName)+"/search/"+"p"+str(pageNum)+"_酒店"
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            page = response.read()
            pageCode = re.sub(r'<br[ ]?/?>', '\n', page)
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None
    def getShopHref(self):
        for i in range(50):
            page = self.getPage(1)
            print page
           soup  = BeautifulSoup(page,'html.parser')
            tags = soup.find("div",id="searchList")
            for j in tags:
               print j

dzdp = DZDP('曼谷')
dzdp.getShopHref()
'''

siteURL = 'http://www.dianping.com'
cityDict = {'曼谷': 'bangkok', '清迈': 'chiangmai', '普吉岛': 'phuket', '苏梅': 'samui', '芭堤雅': 'pattaya'}

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
          'Cookie': '_hc.v="\"4e00da3e-7984-404e-9005-51d405771af2.1473564007\""; PHOENIX_ID=0a030657-15755fea056-7581f5; __utma=1.1087223530.1474615811.1474615811.1474618152.2; __utmb=1.9.10.1474618152; __utmc=1; __utmz=1.1474615811.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); s_ViewType=1; JSESSIONID=F73A761F9822F975B19C7F1A615E00F3; aburl=1; cy=2342; cye=bangkok',
          'Host':'www.dianping.com',
          'Referer': 'http: // www.dianping.com / bangkok / search / _ % E9 % 85 % 92 % E5 % BA % 97',
          'X - Request':'JSON',
          'X - Requested - With':'XMLHttpRequest',
          'Accept': 'application / json, text / javascript',
          'Accept - Encoding':'gzip, deflate, sdch',
          'Accept - Language':'zh - CN, zh;q = 0.8',
          'Cache - Control':'max - age = 0',
          'Connection':'keep - alive'
}
req = {'pageId':'1',
'cityId':'2342',
'shopType':'0',
'categoryId':'0',
'regionId':'0',
'keyword':'按摩'}
url = siteURL+"/"+str(cityDict['曼谷'])+"/search/"+"p"+str(1)+"_%E6%8C%89%E6%91%A9"
#url = "http://www.dianping.com/bangkok/search/p1_%E6%8C%89%E6%91%A9"
request = urllib2.Request(url,headers=header)
response = urllib2.urlopen(request)
page = response.read()
print page

