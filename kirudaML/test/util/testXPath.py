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
url = 'http://finance.naver.com/item/frgn.nhn?code=004650'
#네이버시세 - 매도 호가
#xPath = '//*[@id="content"]/div[2]/table[1]/tbody/tr[4]/td//*[contains(@class, "tah")]/text()'

xPath = '//*[@id="content"]/div[2]/table[1]//tr[5]//*[contains(@class, "tah")]/text()'
         

result = htmlParser.xPathParse(url, xPath)

i = 0
for x in result:
    print("%d : " % i)
    #print(x)
    print(stringController.cleanUpString(x))
    #print(x[39:])
    i = i + 1
    