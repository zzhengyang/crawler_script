README
===========
crawler.py文件用来对蚂蜂窝、大众点评、携程的曼谷、清迈、普吉岛、苏梅、芭堤雅5个地区进行数据采集。     


> 用到的包：  
1. BeautifulSoup包，用来根据URL获取静态页面中的元素信息  
        参考资料：Python爬虫HTML分析，BeautifulSoup库中文文档：http://beautifulsoup.readthedocs.io/zh_CN/latest/#  
        Python结合BeautifulSoup抓取知乎数据：http://blog.csdn.net/u012286517/article/details/51212268  
        BeautifulSoup用法:http://cuiqingcai.com/1319.html  
2. Ghost包，用来根据页面的url动态加载js，获取加载之后的页面代码，并且得到图片标签的src属性  
        参考资料:http://www.2cto.com/kf/201401/273914.html
3. urllib2包，抓取页面并返回页面HTML