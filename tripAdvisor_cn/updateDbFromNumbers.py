# coding=utf-8
import MySQLdb
import xlrd

bioList = []
data = xlrd.open_workbook("/Users/Zyang/Documents/merchants_bio/qingmai_bio.xlsx")
for i in range(0,5):
    table = data.sheet_by_index(i)
    nrows = table.nrows
    for i in range(nrows):
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
cur = conn.cursor()
tuplelist = []
bioList1 = bioList
for i in range(len(bioList1)):
    tuplelist.append(tuple(bioList1[i]))

for i in bioList1:
    cur.execute("update merchants set description='%s',bio='%s' where name='%s' and city_id=4" % (i[1],i[2],i[0]))
    conn.commit()
    print "+1"
cur.close()
conn.close()
