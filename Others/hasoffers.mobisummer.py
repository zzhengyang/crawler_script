# coding:utf8
import os
import re
import urllib2
from datetime import datetime

import configparser
import time
from tqdm import trange
import httplib

USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B100 Safari/602.1'
HEADERS = {'User-Agent': USER_AGENT}
ORIGINAL_URL = 'http://hasoffers.mobisummer.com/aff_c?offer_id=30476&aff_id=4545'

def getPage():
    try:
        url = ORIGINAL_URL
        request = urllib2.Request(url, headers=HEADERS)
        response = urllib2.urlopen(request)
        page = response.read()
        pageCode = re.sub(r'<br[ ]?/?>', '\n', page)
        return pageCode
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            print e.reason


def asoSimulator(file, times):
    httplib.HTTPConnection.debuglevel = 0
    '''
    200正常状态码不会有跳转 也就不会有location
    conn = httplib.HTTPConnection("tu.duowan.com") #这里是host
    conn.request('GET', '/m/meinv/index.html')#上面是分支 注意是GET
    '''
    for i in trange(0, times):
        try:
            getPage()
        except:
            continue
        try:
            requestIp = urllib2.Request('https://ifconfig.co/ip')
            ip = urllib2.urlopen(requestIp)

            file.write(ip.read())
        except:
            file.write("")


def timeMonitor(beginTime):
    afterRunTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if afterRunTime == beginTime:
        return True  # not run
    return False  # have run


def config():
    file_object = open('./usedIp.txt', 'a')
    cf = configparser.ConfigParser()
    cf.read('config.cfg')
    runTimeList = dict(cf.items('config'))
    timeHour = 100

    while True:

        if int(timeHour) != int(time.strftime("%H")):
            asoSimulator(file_object, int(runTimeList[time.strftime("%H")]))
            time.sleep(0.5)
            timeHour = time.strftime("%H")
        time.sleep(1)

    file_object.close()


if __name__ == '__main__':
    config()
