# coding=utf-8
import MySQLdb
import xlrd
item = [7,8,9,10,11,12,13,14]       #按摩
# item = [27,28,29,30,31,32,33,39]       #酒吧
# item = [14,15,16]       #夜店
# item = [21,22,23,24,25,26]      #表演
# item = [17,18,19,20]        #夜市
# item = [34,35,36,37,38]     #红灯区
bioList = []
data = xlrd.open_workbook("/Users/Zyang/Documents/merchants_ima2/mangu.xlsx")
# for i in range(0,4):
table = data.sheet_by_index(1)
nrows = table.nrows
for i in range(1, nrows):
    a = table.row_values(i)
    if not a[0]:
        continue
    bioList.append(a)
print len(bioList)

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
cur.execute("SELECT id,name FROM merchants")
merchantResult = cur.fetchall()
for i in merchantResult:
    merchantList.append(list(i))

for i in bioList:       #[name,des,bio,(****)]
    for j in range(3, 11):
        if i[j] == "":
            continue
        else:
            for k in merchantList:
                if i[0] in k[1]:
                    cur.execute("select * from merchant_categories where merchant_id =%d and category_id=%d"%(k[0],item[j-3]))
                    results = cur.fetchone()

                    if results is not None:
                        print "已存在"
                        continue
                    else:
                        try:
                            # cur.execute("insert into merchant_categories(merchant_id,category_id) VALUES (%d,%d)"%(k[0],item[j-3]))
                            # conn.commit()
                            print i[0].encode('utf8')+"====="+ str(k[0]) + "=====" + str(item[j - 3])
                            break
                        except:
                            continue
                else:
                    continue
cur.close()
conn.close()
