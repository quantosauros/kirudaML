# -*- coding: utf-8 -*-
'''
Created on 2015. 5. 12.

@author: Jay
'''

from bs4 import BeautifulSoup
import urllib2
from util import htmlParser
#from test.HTMLParse import HTMLParse

url = 'http://www.krx.co.kr/m2/m2_1/m2_1_11/JHPKOR02001_11.jsp'
regularExp1 = ["id", "se_key"]

page = urllib2.urlopen(url)

soup = BeautifulSoup(page, from_encoding="utf8")

str = soup.find_all(regularExp1[0], regularExp1[1])

i = 0
for x in str:
    print("%d : " % i)
    print(x.encode('utf8'))
    #print(x.text)
    i = i + 1
