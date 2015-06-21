# -*- coding: utf8 -*-
'''
Created on 2015. 5. 26.

@author: Jay
'''

from lxml import html
from util.htmlParser import htmlParser
from util.stringController import stringController

stockCodeList = ('083570', '005930')
isu_nm = ('호텔신라 [008770]','삼성전자[005930]')
stockCode = ('KR7008770000', 'KR7005930003')

#url = 'http://www.krx.co.kr/m2/m2_1/m2_1_11/JHPKOR02001_11.jsp?isu_cd=' + stockCodeList[1]
url = 'http://www.krx.co.kr/m2/m2_1/m2_1_4/JHPKOR02001_04.jsp'
xPath = '//*[@id="se_key"]'
         
htm = html.parse(url)
result = htm.xpath(xPath)
se_key = result[0].value
print(se_key)
for index in range(0, 2):
    #stockCode = 'KR7' + stockCodeList[1] + '003'
    fr_work_dt ='20150108'
    to_work_dt ='20150108'

    url2 = 'http://www.krx.co.kr/por_kor/corelogic/process/m2/m2_1/m2_1_4/hpkor02001_04.xhtml?data-only=true' + \
        '&se_key=' + se_key + \
        '&isu_nm=' + isu_nm[index] +\
        '&isu_cd=' + stockCode[index] + \
        '&mthd=' + \
        '&fr_work_dt=' + fr_work_dt +\
        '&to_work_dt=' + to_work_dt + \
        '&searchBtn=' + \
        '&searchBtn2=%EC%A1%B0%ED%9A%8C'
    
    htm2 = html.parse(url2)
    print(htm2)
    xpath2 = '//text()'
    result2 = htm2.xpath(xpath2)
    print(result2)
    xpath3 = '//*[contains(@class, "down")]'
    result3 = htm2.xpath(xpath3)
    print(len(result3))
    
    i = 0
    for x in result2:
        print(repr(i) + ": " + x.encode('utf8'))
        i = i + 1

    