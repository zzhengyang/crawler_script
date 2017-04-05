# coding=utf-8
import json
import re

import MySQLdb
import xlrd


# def replaceTime(office_hours):
#     preOfficeHours = office_hours.encode('utf8') \
#         .replace("上午", "am").replace("下午", "pm") \
#         .replace("点", ":").replace("分", "").replace("周末", "weekend").replace("至", "-") \
#         .replace("深夜", "late-night").replace("凌晨", "Am").replace("周日", "Sun") \
#         .replace("每日", "").replace("每天", "").replace("周一", "Mon").replace("周二", "Tue") \
#         .replace("周三", "Wed").replace("周四", "Thu").replace("周五", "Fri").replace("周六", "Sat") \
#         .replace("\n", "")
#     # for i in re.findall('pm(.*?):',preOfficeHours):
#     #     re.sub('(.*?)',)
#     print  re.sub('pm(.*?):', lambda m:str(int(m[0])+12), preOfficeHours)


UPDATE_TYPE = 'merchant'
bioList = []
data = xlrd.open_workbook("/Users/Zyang/Documents/merchants_ima2/merchant_en/puji.xlsx")
for i in range(0,6):
    table = data.sheet_by_index(i)
    nrows = table.nrows
    for i in range(1, nrows):
        a = table.row_values(i)
        if not a[0]:
            continue
        bioList.append(a)

conn = MySQLdb.connect(
    host='139.129.218.173',
    user='dev',
    passwd='123456',
    db='dtrip',
    port=3306,
    charset="utf8"
)
merchantList = []
cur = conn.cursor()
cur.execute("SELECT id,name,office_hours from merchants")
merchantResult = cur.fetchall()
for i in merchantResult:
    merchantList.append(list(i))
a=0
for i in merchantList:
    for j in bioList:
        if i[1] in j[0]:
            cur.execute("SELECT * FROM translations WHERE owner_id=%d" % int(i[0]))
            results = cur.fetchone()
            if results is not None:
                print "已存在"
                continue
            else:
                try:
                    dict = {}.fromkeys(['name', 'bio', 'description','office_hours'])
                    dict['name'] = j[1].encode('utf8').replace('"','').replace("'","")
                    dict['bio'] = j[3].encode('utf8').replace('"','').replace("'","")
                    dict['description'] = j[2].encode('utf8').replace('"','').replace("'","")
                    preOfficeHours = i[2].encode('utf8')\
                        .replace("上午","").replace("下午","pm")\
                        .replace("点",":").replace("分","").replace("周末","weekend").replace("至","-")\
                        .replace("深夜","late-night").replace("凌晨","Am").replace("周日","Sun")\
                        .replace("每日","").replace("每天","").replace("周一","Mon").replace("周二","Tue")\
                        .replace("周三","Wed").replace("周四","Thu").replace("周五","Fri").replace("周六","Sat")\
                        .replace("\n","")
                    dict['office_hours'] = preOfficeHours
                    jsonStr = json.dumps(dict)
                    cur.execute("INSERT INTO translations(owner_type,owner_id,data,lang) VALUES ('%s',%d,'%s','%s')" % (\
                    UPDATE_TYPE, int(i[0]), jsonStr,"en-US"))
                    conn.commit()
                    print i[1]
                    print dict['description']
                    print dict['bio']
                    a+=1
                # print dict['bio']
                # print dict['description']
                # print '+1'
                    break
                except :
                    print "error"
                    continue
cur.close()
conn.close()
print a
