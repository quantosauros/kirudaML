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
url = 'http://www.krx.co.kr/m2/m2_1/m2_1_11/JHPKOR02001_11.jsp?isu_cd=041830'
#네이버시세 - 매도 호가
#xPath = '//*[@id="content"]/div[2]/table[1]/tbody/tr[4]/td//*[contains(@class, "tah")]/text()'

xPath = '//*[@id="se_key"]'
         

result = htmlParser.xPathParse(url, xPath)

i = 0
for x in result:
    print("%d : " % i)
    print(x.value)
    #print(stringController.cleanUpString(x))
    #print(x[39:])
    i = i + 1
    