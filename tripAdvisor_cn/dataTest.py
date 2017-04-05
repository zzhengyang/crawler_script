#coding:utf8
import json
import re
import traceback
import urllib2

import MySQLdb


def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False
class enToCn:
    def __init__(self):
        self.website = 'http://api.heylotus.com/merchants'
        self.headers = {'Accept-Language':'en-US'}
    def getPage(self,url):
        try:
            Url = self.website+url
            request = urllib2.Request(Url, headers=self.headers)
            response = urllib2.urlopen(request)
            page = response.read()
            pageCode = re.sub(r'<br[ ]?/?>', '\n', page)
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

test = enToCn()
a=0
conn = MySQLdb.connect(
    host='139.129.218.173',
    user='dev',
    passwd='123456',
    db='dtrip',
    port=3306,
    charset="utf8"
)
cur = conn.cursor()
# for city in range(1,5):
    # for cat in range(1,7):
    #     for pageNum in range(1,31):
page = test.getPage("?per-page=500&sort=distance&_coordinate=50,50")

jsonResult = json.loads(str(page))
for i in jsonResult['items']:
    print i

                # for text in i['office_hours']:
                #     if is_chinese(text):
                #         cur.execute("select data from translations where owner_type='%s' and owner_id=%d"%('merchant',i['id']))
                #         enResult1 = cur.fetchone()
                        # try:
                        #     enResult = json.loads(enResult1[0])
                        #
                        #     dict = {}
                        #     if 'name' in enResult.keys():
                        #         dict['name'] = enResult['name']
                        #     else:
                        #         # dict['bio'] = enResult['bio']
                        #         # dict['description'] = enResult['description']
                        #         preOfficeHours = i['office_hours']\
                        #             .encode('utf8')\
                        #             .replace("上午", "").replace("下午", "pm") \
                        #             .replace("点", ":").replace("分", "").replace("周末", "weekend").replace("至", "-") \
                        #             .replace("深夜", "late-night").replace("凌晨", "Am").replace("周日", "Sun") \
                        #             .replace("每日", "").replace("每天", "").replace("周一", "Mon").replace("周二", "Tue") \
                        #             .replace("周三", "Wed").replace("周四", "Thu").replace("周五", "Fri").replace("周六", "Sat") \
                        #             .replace("\n", "")
                        #         dict['office_hours'] = preOfficeHours
                        #         # dict['bio'] = MySQLdb.escape_string(dict['bio'])
                        #         # dict['description'] = MySQLdb.escape_string(dict['description'])
                        #
                        #         jsonStr = json.dumps(dict)
                        #
                        # #
                        # #         # cur.execute("UPDATE translations set data='%s' where owner_type='%s' and owner_id=%d"%(MySQLdb.escape_string(jsonStr),'merchant',i['id']))
                        # #         # conn.commit()
                        # #
                        # #
                        #         print MySQLdb.escape_string(jsonStr)
                        #         a += 1
                        #
                        # #         print "+1"
                        # except:
                        #     # traceback.print_exc()
                        #     # continue
                        #     break
                    #     print i['name']
                    #     print i['id']
                    #     print i['office_hours']
                    #
                    # break
                # if is_chinese(i['bio']) or is_chinese(i['description']):
                #     print str(i['id'])+"=="+str(i['city_id'])+"=="+str(i['category_id'])+"=="+i['name']


print a
cur.close()
conn.close()