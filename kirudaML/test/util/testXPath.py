# -*- coding: cp949 -*-
'''
Created on 2015. 5. 26.

@author: Jay
'''

from lxml import html
from util.htmlParser import htmlParser


#�ð����ü�
#url = 'http://finance.naver.com//item/sise_time.nhn?code=008770&thistime=20150526125212'
#xPath = '//span[@class="tah p10 gray03"]/text()'
#xPath = '//span[@class="tah p11"]/text()'
#���Ϻ�
#xPath = '//span[@class="tah p11 red02"]/text()'

#���̹��ü�
#url = 'http://finance.naver.com/item/sise.nhn?code=008770&asktype=10'
url = 'http://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page=1'
#���̹��ü� - �ŵ� ȣ��
#/html/body/table[1]/tbody/tr[3]/td[1]/span
xPath = '//*[@class="pgRR"]/a/@href'
         
         
#���̹��ü� - �ż� ȣ��
#xPath = '//span[@class="tah p11 red01"]/text()'
#
#xPath = '//span[@class="tah p11"]/text()'
#xPath = '//strong[@class="tah p11"]/text()'

result = htmlParser.xPathParse(url, xPath)

i = 0
for x in result:
    print("%d : " % i)
    print(x)
    print(x[39:])
    i = i + 1
    