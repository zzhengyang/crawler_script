# coding:utf8
import json
import os
import re
import traceback
import urllib
import urllib2

import MySQLdb





user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
headers = {'User-Agent': user_agent}



conn = MySQLdb.connect(
    host='139.129.218.173',
    user='dev',
    passwd='123456',
    db='dtrip',
    port=3306,
    charset="utf8"
)
cur = conn.cursor()
cur.execute("SELECT name,merchant_ids FROM topics where status=1")
results = cur.fetchall()
idList = []
for i in results:
    # dir = i[0]
    # os.makedirs("/Users/Zyang/Documents/dtrip/merchants_ima/topics_ima/" + dir)
    idList.append(i[1])

def downLoadIma(idList):
    a = 0
    for merchantIdList1 in idList:
        # for merchantIdList in merchantIdList1:
        print str(merchantIdList1)
            # cur.execute("")
            # cur.execute("SELECT content_image_url FROM merchants WHERE id=%d" % merchantIdList)
            # result2 = cur.fetchone()
            # # urlList = list(result2)[0]
            # # data1 = json.loads(urlList)
            # # data2 = list(data1.values())
            # imaURL =  result2
            # print imaURL[0]
#             try:
#                 # url = j.encode("utf-8")
# #                     redata = url.replace("/", "|")
#                 path = "/Users/Zyang/Documents/dtrip/merchants_ima/topics_ima/" + str(imaURL[0])+".jpg"
#                 request = urllib2.Request(imaURL[0], headers=headers)
#                 f = urllib2.urlopen(request)
#                 data = f.read()
#                 z = file(path,"wb")
#                 z.write(data)
#                 z.close()
#                 print "success"
#                 a += 1
#                 print path
#
#             except:
#                 traceback.print_exc()
    #     else:
    #         print "已下载"
    #         continue
    # print "共下载" + str(a) + "条"

#
def mkdir(list):
    for i in list:
        print i
        path = "/Users/Zyang/Documents/dtrip/merchants_ima/topics_ima/" + str(i[0])
        try:
            isExists = os.path.exists(path)

            if not isExists:
                os.makedirs(path)
        except OSError, e:
            print "e"


# mkdir(idList)
downLoadIma(idList)




