#coding:utf8
import os
import re

import MySQLdb

conn = MySQLdb.connect(
    host='139.129.210.170',
    user='root',
    passwd='123456',
    db='app',
    port=3306,
    charset="utf8"
)
cur = conn.cursor()


file = open("/Users/Zyang/Documents/ASO/AppStore/appstore_0118_20000.txt")
a = 0
account = []
for line in file:
    a = []
    pattern = re.findall(r'.*?@163.com',line)
    pattern_pas = re.findall(r'@163.com(.*?)question1',line)
    if pattern:
        a.append(pattern[0])
        pattern22= str(pattern_pas[0]).replace("\t",'')
        a.append(pattern22)
        account.append(a)
b=0
boss = []
for i in range(0,len(account)):
    cur.execute("UPDATE app_info set appStoreId=%s,appStorePwd=%s where id=%s",(account[i][0],account[i][1],20000-i))
    conn.commit()
    print account[i]
    b+=1
    print b

print b
# for i in range(0,5):
#     cur.execute("update app_info set appStoreId='%s' where id = "%i)
#     cur.execute("insert into app_info(appKey,appId,title,appDesc,appStoreId,appStorePwd)\
#                               values  ('%s','%s','%s','%s','%s','%s')"\
#                               %("蜘蛛纸牌","com.katchapp.solitaire011","纸牌接龙","sanhao",line,"Qq778899"))
#     conn.commit()
#     a+=1
#     print a

# def echoJson(startNum,endNum):
#     a = '[{"id":1,"proxy_url":"http://xx.xx","proxy_port":1234,"config_url":"http://139.129.210.170/raw/api/app/app'+str(startNum)+'.php"},'
#     for i in range(2,100):
#         a += '{"id":' + str(
#             i) + ',"proxy_url":"http://xx.xx","proxy_port":1234,"config_url":"http://139.129.210.170/raw/api/app/app' + str(
#             startNum+i-1) + '.php"},'
#     a += '{"id":100,"proxy_url":"http://xx.xx","proxy_port":1234,"config_url":"http://139.129.210.170/raw/api/app/app'+str(endNum)+'.php"}]'
#
#     return a
#
# print echoJson(901,1000)


# for i in range(1,11):
#     os.mkdir("/Users/Zyang/Documents/appStoreSSH/test/"+str(i))
# coding:utf8



