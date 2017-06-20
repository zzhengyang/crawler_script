# coding:utf8
import sys
import re
import urllib2
import cookielib

USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B100 Safari/602.1'
HEADERS = {'User-Agent': USER_AGENT}
COOKIE_FILE = 'cookie.txt'


def getPage():
    try:
        url = sys.argv[1]
        request = urllib2.Request(url, headers=HEADERS)

        response = urllib2.urlopen(request)

        page = response.read()
        pageCode = re.sub(r'<br[ ]?/?>', '\n', page)
        return pageCode
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            print e.reason

class SimpleCookieHandler(urllib2.BaseHandler):
    def http_request(self, req):
        simple_cookie = 'cc98Simple=1'
        if not req.has_header('Cookie'):
            req.add_unredirected_header('Cookie', simple_cookie)
        else:
            cookie = req.get_header('Cookie')
            req.add_unredirected_header('Cookie', simple_cookie + '; ' + cookie)
        return req

def getPageWithCookie():
    cookie = cookielib.MozillaCookieJar(COOKIE_FILE)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie), SimpleCookieHandler())
    requestUrl = 'http://www.apxadtracking.net/iclk/redirect.php?apxcode=437243&id=eWJrKN9QmzjMIWuXeUjnmToUKOjMIWuXeWeQeWj-0N'
    req = urllib2.Request(requestUrl, headers=HEADERS)
    result = opener.open(req)
    print cookie._cookies.values()
    # 保存cookie到cookie.txt中
    cookie.save(ignore_discard=True, ignore_expires=True)

    # 利用cookie请求访问另一个网址

    # gradeUrl = 'http://hasoffers.mobisummer.com/aff_c?offer_id=30476&aff_id=4545'

    # result = opener.open(gradeUrl)
    # print result.read()

def a():
    cookie = cookielib.MozillaCookieJar(COOKIE_FILE)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler, SimpleCookieHandler())
    # opener.open('http://www.baidu.com')
    opener.open(
        'http://www.apxadtracking.net/iclk/redirect.php?apxcode=437243&id=eWJrKN9QmzjMIWuXeUjnmToUKOjMIWuXeWeQeWj-0N')
    print cookie._cookies.values()
    cookie.save(ignore_discard=True, ignore_expires=True)


if __name__ == '__main__':
#     # getPage()
    getPageWithCookie()
    # a()
