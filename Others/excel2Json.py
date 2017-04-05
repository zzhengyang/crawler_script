# -*- coding: utf-8 -*-
import json
from datetime import datetime
from datetime import timedelta
import xlrd
import sys


from tqdm import trange

reload(sys)
sys.setdefaultencoding('utf-8')

def readFile(filename):
    data = xlrd.open_workbook(filename)

    table = data.sheet_by_index(1)
    jobList = []

    for i in trange(0,30):
        jsonDict = {}.fromkeys(('date', 'url', 'hours'))

        d1 = datetime.now() + timedelta(days=i)
        d2 = d1.strftime('%Y-%m-%d') + ' 00:00:00'
        jsonDict['date'] = d2

        jsonDict['url'] = 'http://www.baidu.com'
        hourList = []
        for j in trange(0,23):
            hourList.append(int(table.cell(i+11, j+2).value))
        jsonDict['hours']  = hourList

        jobList.append(jsonDict)
    return json.dumps(jobList)

result = readFile('/Users/Zyang/Desktop/cpa模型_20170331.xlsx')

file_object = open('./raw.config.json', 'w+')
file_object.write(result)
file_object.close()
