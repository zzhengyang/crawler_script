import urllib
import json
import socket
socket.setdefaulttimeout(10)
proxys = []
proxys.append({"http":"http://119.6.136.122"})
proxys.append({"http":"http://202.155.210.2"})
proxys.append({"http":"http://115.211.238.77"})
proxys.append({"http":"http://39.67.92.122"})
proxys.append({"http":"122.228.179.178"})
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
          'Cookie': '_hc.v="\"4e00da3e-7984-404e-9005-51d405771af2.1473564007\""; PHOENIX_ID=0a030657-15755fea056-7581f5; __utma=1.1087223530.1474615811.1474615811.1474618152.2; __utmb=1.9.10.1474618152; __utmc=1; __utmz=1.1474615811.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); s_ViewType=1; JSESSIONID=F73A761F9822F975B19C7F1A615E00F3; aburl=1; cy=2342; cye=bangkok',
          'Referer': 'http: // www.dianping.com / bangkok / search / _ % E9 % 85 % 92 % E5 % BA % 97',
          'X - Request':'JSON',
          'X - Requested - With':'XMLHttpRequest'}
for id in range(5):
    try:
        url = "http://www.dianping.com/bangkok/search/_%E9%85%92%E5%BA%97"
        res = urllib.urlopen(url,proxies=proxys[id%5]).read()
        print res
    except Exception,e:
        print e
        continue