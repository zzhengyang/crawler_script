from ghost import Ghost
from bs4 import BeautifulSoup
import urllib2

url = 'http://www.mafengwo.cn/photo/poi/6022130.html'
ghost = Ghost(wait_timeout=120)
page, resources = ghost.open(url)
print ghost.content


