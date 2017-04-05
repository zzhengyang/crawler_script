# coding:utf-8
import MySQLdb


def is_chinese():
    """判断一个unicode是否是汉字"""
    a = 0
    conn = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='root',
        db='dtrip',
        port=3306,
        charset="utf8"
    )
    cur = conn.cursor()
    cur.execute("select id,content from comments_cn")
    comments = cur.fetchall()
    for i in comments:
        idAndContentList = list(i)
        # print idAndContentList[1]
        for j in idAndContentList[1]:
            if j >= u'\u4e00' and j <= u'\u9fa5':
                print "isChinese"
                a += 1
                break

            else:
                cur.execute("delete from comments_cn where id=%d"%int(idAndContentList[0]))
                conn.commit()
                break
    cur.close()
    conn.close()

is_chinese()
