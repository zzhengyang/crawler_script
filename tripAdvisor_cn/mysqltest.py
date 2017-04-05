# coding=utf-8
import os
import os.path
import MySQLdb


conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            passwd='root',
            db='dtrip',
            port=3306,
            charset="utf8"
        )
cur = conn.cursor()
# cur.execute("INSERT INTO locations(name,description,city_id,coordinate)\
#                       VALUES('%s', '%s'    ,%d    , ST_POINTFROMTEXT('POINT(%f %f)'))"\
#                     %('娜娜广场','哈哈',1,100.553009,13.741428))
# # cur.execute("INSERT INTO locations(name,city_id) values")
# conn.commit()
# cur.close()
# conn.close()

def GetFileList(dir, fileList):
    newDir = dir
    # if os.path.isfile(dir):
    #     fileList.append(dir)
    # el
    if os.path.isdir(dir):
        for s in os.listdir(dir):
        # 如果需要忽略某些文件夹，使用以下代码
        # if s == "xxx":
        # continue
            fileList.append(s)
            newDir = os.path.join(dir, s)
            # GetFileList(newDir, fileList)


    return fileList

lists = GetFileList('/Users/Zyang/Downloads/merchants_ima', [])


for i in lists:
    reimage = ''
    mypath = '/Users/Zyang/Downloads/merchants_ima/' + i
    try:
        for f in os.listdir(mypath):
            if f == ".DS_Store":
                continue
            reimage = f
    except:
        continue
    image = reimage.replace("|","/")
    cur.execute("UPDATE merchants_cn SET content_image_url='%s' WHERE name='%s' " %\
                (image,i))
    conn.commit()
cur.close()
conn.close()