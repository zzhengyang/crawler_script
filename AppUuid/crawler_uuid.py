# coding:utf-8
import time


import time
from string import zfill

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.common.exceptions import UnexpectedAlertPresentException

# BrowserObj_dirver = webdriver.Chrome()
#
# BrowserObj_dirver.get("https://lastpass.com/udid/")

#BrowserObj_dirver.implicitly_wait(3)

def uuid_crawler(startIndex):
# startIndex = 14403

    while True:
        retryNum = 0

        try:
            BrowserObj_dirver = webdriver.Chrome()

            BrowserObj_dirver.get("https://lastpass.com/udid/")
            EditObj_element = BrowserObj_dirver.find_element_by_id('mypassword')

            for i in range(startIndex,65536):
                startIndex = i
                if retryNum > 20:
                    BrowserObj_dirver.quit()
                    break

                num = hex(i).replace('0x','').zfill(4)
                EditObj_element.send_keys(num)
                EditObj_element.send_keys(Keys.RETURN)
                time.sleep(1)

                f = open('/Users/Zyang/Documents/ASO/appUUID/' + str(num) + '.txt', 'w')
                f.write(BrowserObj_dirver.page_source.encode('utf-8'))
                f.close()
                print i, num
                while True:
                    try:
                        EditObj_element.clear()
                        retryNum = 0
                        break
                    except Exception as e:
                        time.sleep(1)
                        print 'retry'
                        retryNum = retryNum + 1
                        if retryNum > 20 :
                            break
        except UnexpectedAlertPresentException as e:
            print e



