#coding:utf-8

# for num in range(901,1001):
#         a = ',{"id":'+str(num-900)+',"proxy_url":"http://xx.xx","proxy_port":1234,"config_url":"http://139.129.210.170/raw/api/app/app'+str(num)+'.php","vpn_config":{"server_ip" :"59.110.137.125", "type":"IPSec" ,"username": "heylotus1","ip_psk" : "EfD7uv8z7JDN42K8","password"  : "heylotus1"}}'
#         print a
import os

import MySQLdb
from bs4 import BeautifulSoup



# import re
#
# halfHtmlText = '<html><head><title>Test<!----></title><!----></head><body><h1>Parse me!</h1></body><!-----123123-->'
# fullHtmlText = '<html><head><title>Test<!----></title></head><body><h1>Parse me!</h1></body></html>   <!---123123---->zzz'
#
# def checkHtmlValidation(htmlText):
#     re_comment = re.compile('<!--[^>]*-->')
#     re_endspace = re.compile('</html>(.*?)$')
#     # noAnnotationHtml = re.sub(re_comment,'',htmlText)
#     noSpaceHtml = re.sub(re_endspace,'',htmlText)
#     return noSpaceHtml
#     # return noAnnotationHtml
#     # if noSpaceHtml.endswith("</html>"):
#     #     return True
#     # return False
# print checkHtmlValidation(fullHtmlText)
#
NUMBER = 400
JOB = 50
path = '/Users/Zyang/Documents/job/'
for job in range(1,JOB+1):
    opath = path+str(job)+'/'
    print str(job)+"\n============"
    file_object = open(opath+'job.json', 'w')

    s = '[{"id":'+str(1)+',"proxy_url":"http://xx.xx","proxy_port":1234,"config_url":"http://139.129.210.170/raw/api/app/app'+str(job*NUMBER-NUMBER+1)+'.php","vpn_config":{"server_ip" :"59.110.137.125", "type":"IPSec" ,"username": "heylotus1","ip_psk" : "EfD7uv8z7JDN42K8","password"  : "heylotus1"}}'
    e = ',{"id":'+str(NUMBER)+',"proxy_url":"http://xx.xx","proxy_port":1234,"config_url":"http://139.129.210.170/raw/api/app/app'+str(job*NUMBER)+'.php","vpn_config":{"server_ip" :"59.110.137.125", "type":"IPSec" ,"username": "heylotus1","ip_psk" : "EfD7uv8z7JDN42K8","password"  : "heylotus1"}}]'
    for i in range(2,NUMBER):
        s+= ',{"id":'+str(i)+',"proxy_url":"http://xx.xx","proxy_port":1234,"config_url":"http://139.129.210.170/raw/api/app/app'+str(job*NUMBER-NUMBER+i)+'.php","vpn_config":{"server_ip" :"59.110.137.125", "type":"IPSec" ,"username": "heylotus1","ip_psk" : "EfD7uv8z7JDN42K8","password"  : "heylotus1"}}'

    file_object.write(s+e)
    file_object.close()

# path = '/Users/Zyang/Documents/app/'
# for i in range(1,20001):
#     opath = path+'app'+str(i)+'.php'
#
#     print opath
#     file_object = open(opath, 'w')
#     s = '<?php        header("content-type:text/html; charset=utf-8");        define("DB_HOST","localhost");        define("DB_USER","root");        define("DB_PWD","root");        define("DB_NAME","app");        $connect = mysql_connect(DB_HOST,DB_USER,DB_PWD) or die("error".mysql_error());        mysql_select_db(DB_NAME,$connect) or die("error".mysql_error());        $result = array();        $a=array("vpn_config"=>array("server_ip" =>"59.110.137.125", "type"=>"IPSec" ,"username"=>"heylotus1","ip_psk" => "EfD7uv8z7JDN42K8","password"  => "heylotus1"));        mysql_query("SET NAMES UTF8");        $query = "SELECT appKey,appId,title,appDesc,appStoreId,appStorePwd FROM app_info where id='+str(i)+'";        $mysql = mysql_query($query) or die("error".mysql_error());        while($row = mysql_fetch_array($mysql,MYSQL_ASSOC)){                array_push($row,$a);                array_push($result,$row);        }        echo json_encode($result,JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES);        mysql_free_result($mysql);?>'
#     file_object.write(s)
#     file_object.close()

# conn = MySQLdb.connect(
#             host='139.129.210.170',
#             user='root',
#             passwd='123456',
#             db='app',
#             port=3306,
#             charset="utf8"
#         )
# cur = conn.cursor()
# values=[]
# for i in range(0,17455):
#     values.append(('蜘蛛纸牌', 'com.katchapp.solitaire011', '纸牌接龙', 'sanhao', '123123@126.com', 'Qq112211'))
#
# cur.executemany("insert into app_info(appKey,appId,title,appDesc,appStoreId,appStorePwd) values (%s,%s,%s,%s,%s,%s)",values)
# conn.commit()

