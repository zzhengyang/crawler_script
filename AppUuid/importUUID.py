import os
import re
import MySQLdb
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import crawler_uuid
def import_uuid():
    # BrowserObj_dirver = webdriver.Chrome()
    #
    # BrowserObj_dirver.get("https://lastpass.com/udid/")
    # EditObj_element = BrowserObj_dirver.find_element_by_id('mypassword')
    conn = MySQLdb.connect(
                host='127.0.0.1',
                user='root',
                passwd='root',
                db='aso',
                port=3306,
                charset="utf8"
            )
    cur = conn.cursor()
    rootDir = '/Users/Zyang/Documents/ASO/fail_crawler_cong4/'
    failList = []
    a = 0
    for lists in os.listdir(rootDir):
        # if int(str(lists).replace('.txt', ''), 16)>34149:
            if lists == '.DS_Store':
                continue
            path = os.path.join(rootDir, lists)
            f = open(path)
            ff = f.read()
            soup = BeautifulSoup(ff, 'html.parser')
            try:
                preDiv =  str(soup.findAll("pre")[0])
                UDES = re.findall('UDID:.*: (.*)',preDiv)
                UDID = re.findall('UDID: (.*?):',preDiv)
                udList = []
                for i in range(len(UDID)):
                    udList.append((UDID[i],UDES[i]))
                cur.executemany("insert into apple_account(udid,equ_name) VALUES (%s,%s)",udList)
                conn.commit()
                a+=1
                print a
            except:
                # EditObj_element.send_keys(str(lists).replace('.txt', ''))
                # EditObj_element.send_keys(Keys.RETURN)
                # time.sleep(1)
                #
                # f = open('/Users/Zyang/Documents/ASO/fail_crawler_cong4/' + str(lists), 'w')
                # f.write(BrowserObj_dirver.page_source.encode('utf-8'))
                # f.close()
                # # print 'fail'
                #
                # while True:
                #     try:
                #         EditObj_element.clear()
                #
                #         break
                #     except Exception as e:
                #         time.sleep(1)
                #         print 'retry'
                #
                # print lists, int(str(lists).replace('.txt', ''), 16)
                failList.append(lists)
                continue
        # else:
        #     continue
    print failList
import_uuid()
