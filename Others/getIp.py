# coding:utf8
import urllib2

USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B100 Safari/602.1'
HEADERS = {'User-Agent': USER_AGENT}

def getIp():
    try:
        requestIp = urllib2.Request('https://ifconfig.co/ip')
        ip = urllib2.urlopen(requestIp)
        return ip.read()
    except:
        pass

if __name__ == '__main__':
    print getIp()