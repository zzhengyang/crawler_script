# coding=utf-8
import MySQLdb
import xlrd
import xlsxwriter

conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            passwd='root',
            db='cq_aso',
            port=3306,
            charset="utf8"
        )
cur = conn.cursor()
path_des = "/Users/Zyang/Documents/ASO/dropFile2/"
cur.execute("SELECT DISTINCT query_date from keyword_day")
dateResult = cur.fetchall()
dateList = []
for j in range(len(dateResult)):
    w = xlsxwriter.Workbook(path_des + "Day"+str(j+1).zfill(3)+".xlsx")
    ws = w.add_worksheet('aso')
    cur.execute("SELECT app_id,app_name,app_word,app_rank,app_priority,app_searchcount,query_date from keyword_day where query_date='%s'"%str(dateResult[j][0]))
    result = cur.fetchall()
    for i in range(len(result)):
        ws.write(i, 0, int(result[i][0]))   #app_id
        ws.write(i, 1, result[i][1])    #app_name
        ws.write(i, 2, result[i][2])    #app_word
        ws.write(i, 3, int(result[i][3]))    #word_rank
        ws.write(i, 4, int(result[i][4]))    #priority
        ws.write(i, 5, int(result[i][5]))   #searchcount
        ws.write(i, 6, result[i][6])    #query_date
    w.close()
    print str(dateResult[j][0])
cur.close()
conn.close()