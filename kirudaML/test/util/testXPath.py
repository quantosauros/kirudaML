# -*- coding: cp949 -*-
'''
Created on 2015. 5. 26.

@author: Jay
'''

from lxml import html
from util.htmlParser import htmlParser
from util.stringController import stringController


#�ð����ü�
#url = 'http://finance.naver.com//item/sise_time.nhn?code=008770&thistime=20150526125212'
#xPath = '//span[@class="tah p10 gray03"]/text()'
#xPath = '//span[@class="tah p11"]/text()'
#���Ϻ�
#xPath = '//span[@class="tah p11 red02"]/text()'

#���̹��ü�
#url = 'http://finance.naver.com/item/sise.nhn?code=008770&asktype=10'
url = 'http://finance.naver.com/item/sise.nhn?code=950110'
#���̹��ü� - �ŵ� ȣ��
xPath = '//*[@id="_amount"]/text()'

#xPath = '//*[@id="content"]/div[2]/div[1]/table/tbody/tr/td//*[contains(@class, "tah")]/text()'
         
         
#���̹��ü� - �ż� ȣ��
#xPath = '//span[@class="tah p11 red01"]/text()'
#
#xPath = '//span[@class="tah p11"]/text()'
#xPath = '//strong[@class="tah p11"]/text()'

result = htmlParser.xPathParse(url, xPath)

i = 0
for x in result:
    print("%d : " % i)
    #print(x)
    print(stringController.cleanUpString(x))
    #print(x[39:])
    i = i + 1
    