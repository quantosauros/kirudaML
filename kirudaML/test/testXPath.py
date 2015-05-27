# -*- coding: cp949 -*-
'''
Created on 2015. 5. 26.

@author: Jay
'''

from lxml import html
from util.htmlParser import htmlParser


#시간별시세
#url = 'http://finance.naver.com//item/sise_time.nhn?code=008770&thistime=20150526125212'
#xPath = '//span[@class="tah p10 gray03"]/text()'
#xPath = '//span[@class="tah p11"]/text()'
#전일비
#xPath = '//span[@class="tah p11 red02"]/text()'

#네이버시세
#url = 'http://finance.naver.com/item/sise.nhn?code=008770&asktype=10'
url = 'http://finance.naver.com/item/sise.nhn?code=004650&asktype=10'
#네이버시세 - 매도 호가
#/html/body/table[1]/tbody/tr[3]/td[1]/span
xPath = '//*[@id="content"]/div[2]/div[1]/table/tbody/tr/td[1]/span/text()'
         
#네이버시세 - 매수 호가
#xPath = '//span[@class="tah p11 red01"]/text()'
#
#xPath = '//span[@class="tah p11"]/text()'
#xPath = '//strong[@class="tah p11"]/text()'

result = htmlParser.xPathParse(url, xPath)

i = 0
for x in result:
    print("%d : " % i)
    print(x.strip())
    i = i + 1
    