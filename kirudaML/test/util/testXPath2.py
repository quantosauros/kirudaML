# -*- coding: utf8 -*-
'''
Created on 2015. 5. 26.

@author: Jay
'''

from lxml import html
from util.htmlParser import htmlParser
from util.stringController import stringController

stockCode = '008770'
isu_nm = '호텔신라 [008770]'
url = 'http://www.krx.co.kr/m2/m2_1/m2_1_11/JHPKOR02001_11.jsp?isu_cd=' + stockCode
xPath = '//*[@id="se_key"]'
         
htm = html.parse(url)
result = htm.xpath(xPath)
se_key = result[0].value
print(se_key)

stockCode = 'KR7' + stockCode + '000'
fr_work_dt ='20150611'
to_work_dt ='20150612'
url2 = 'http://www.krx.co.kr/por_kor/corelogic/process/m2/m2_1/m2_1_11/hpkor02001_11.xhtml?data-only=true' + \
    '&gubun=s&se_key=' + se_key + \
    '&jisu_sch_type=1' + \
    '&isu_nm=' + isu_nm +\
    '&isu_cd=' + stockCode + \
    '&mthd=&fr_work_dt=' + fr_work_dt +\
    '&to_work_dt=' + to_work_dt + \
    '&searchBtn=&searchBtn2=%EC%A1%B0%ED%9A%8C'

htm2 = html.parse(url2)
print(htm2)
xpath2 = '//text()'
result2 = htm2.xpath(xpath2)
print(result2)
 
i = 0
for x in result2:
    print(repr(i) + ": " + x)
    i = i + 1
    