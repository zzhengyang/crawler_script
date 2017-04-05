# coding:utf8
import os
import urllib2
import datetime
import Queue
from threading import Thread

import configparser
import time
from tqdm import trange
import httplib

USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B100 Safari/602.1'
HEADERS = {'User-Agent': USER_AGENT}
JOB_NUM = 4000
q = Queue.Queue(maxsize = JOB_NUM)

class JobQueue:
    def queueInit(self):
        for i in range(JOB_NUM):
            d1 = datetime.datetime.now()

            d2 = d1.strftime('%Y-%m-%d') + ' 00:00:00'
            y = datetime.datetime.strptime(d2, '%Y-%m-%d %H:%M:%S')
            jobTime = y + datetime.timedelta(seconds=24 * 3600 / JOB_NUM * i)
            q.put(Job(i, jobTime))
        return q

class Job(object):
    time = datetime.datetime.now()
    def __init__(self, index, time):
        self.index = index
        self.time = time

def asoSimulator():
    file_object = open('./usedIp.txt', 'w+')

    httplib.HTTPConnection.debuglevel = 1
    '''
    200正常状态码不会有跳转 也就不会有location
    conn = httplib.HTTPConnection("tu.duowan.com") #这里是host
    conn.request('GET', '/m/meinv/index.html')#上面是分支 注意是GET
    '''

    conn = httplib.HTTPConnection("atracking-auto.appflood.com")
    conn.request('GET', '/transaction/post_click?offer_id=6152823&aff_id=7300', '',
                 {'user-agent': USER_AGENT})
    responseHeader = conn.getresponse().getheaders()
    for item in responseHeader:
        if item[0] == 'location':
            redictUrl = item[1]
            try:
                request = urllib2.Request(redictUrl, headers=HEADERS)
                f = urllib2.urlopen(request)
                requestIp = urllib2.Request('https://ifconfig.co/ip')
                ip = urllib2.urlopen(requestIp)

                file_object.write(ip.read())
            except urllib2.HTTPError as e:
                continue
    conn.close()
    file_object.close()


jobQueue = JobQueue()
p = jobQueue.queueInit()
def processJob():
    a = 0
    while True:
        job = p.get()

        if job.time > datetime.datetime.now():
            delay = job.time - datetime.datetime.now()
            time.sleep(delay.seconds)
            asoSimulator()
        #         print "index================>", item.index
processJob()

# for i in range(3):
#      t = Thread(target=processJob)
#      t.daemon = True
#      t.start()


