# -*- coding: cp949 -*-
'''
Created on 2015. 5. 26.

@author: Jay
'''

from lxml import html
from util.htmlParser import htmlParser
from util.stringController import stringController

#네이버시세
#url = 'http://finance.naver.com/item/sise.nhn?code=008770&asktype=10'
url = 'http://finance.daum.net/item/trader.daum?code=000250&beforeday=1'
#네이버시세 - 매도 호가
#xPath = '//*[@id="content"]/div[2]/table[1]/tbody/tr[4]/td//*[contains(@class, "tah")]/text()'

xPath = '//*[@id="contentWrap"]/h5/span/span[1]/text()'
         

result = htmlParser.xPathParse(url, xPath)

i = 0
for x in result:
    print("%d : " % i)
    #print(x)
    print(stringController.cleanUpString(x))
    #print(x[39:])
    i = i + 1
    