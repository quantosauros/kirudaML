# -*- coding: cp949 -*-
'''
Created on 2015. 5. 12.

@author: Jay
'''

from bs4 import BeautifulSoup
import urllib2
from util import htmlParser
#from test.HTMLParse import HTMLParse


# Naver 주식종목
url = "http://finance.naver.com/item/main.nhn?code=008770"
# 투자정보
regularExp1 = ["div", "tab_con1", "em"]
# 호가 10단계
reqularExp2= ["div", "tab_con2", "td"]

result1 = htmlParser.htmlParser.parse(url, regularExp1);
# 0 : 시가총액
# 1 : 시가총액순위
# 2 : 상장주식수
# 3 : 액면가
# 4 : 매매단위
# 5 : 외국인한도주식수
# 6 : 외국인보유주식수
# 7 : 외국인소진율
# 8 : 투자의견
# 9 : 목표주가
# 10 : 52주최고
# 11 : 52주최저
# 12 : PER
# 13 : EPS
# 14 : PBR
# 15 : BPS
# 16 : 추정PER
# 17 : EPS
# 18 : 부채비율
# 19 : 동일업종PER
# 20 : 동일업종 등략률
i = 0
for x in result1:
    print("%d : " % i)
    print(x.text)
    i = i + 1





page = urllib2.urlopen(url)
soup = BeautifulSoup(page, from_encoding="euc-kr")

#str = soup.find_all(regularExp1, regularExp2)[0].find_all(regularExp3)
#str = soup.find_all('div', 'tab_con1')[0].find_all('em')
#str = soup.find_all()

#===============================================================================
# i = 0
# for x in str:
#     #print("%d : " % i)
#     print(x.text)
#     i = i + 1
#===============================================================================

#===============================================================================
# str = soup.find_all('div', 'tab_con2')[0].find_all('td')
# 
# i = 0
# for x in str:
#     #print("%d : " % i)
#     print(x.text)
#     i = i + 1
#===============================================================================


#===============================================================================
# html = lxml.html.parse("http://finance.naver.com/item/main.nhn?code=008770")
# packages = html.xpath('//*[@id="_market_sum"]')
# 
# print(packages)
#===============================================================================

#===============================================================================
# url = 'http://finance.naver.com/item/main.nhn?code=008770'
# page = requests.get(url)
# document_tree = lxml.html.fromstring(page.text)
# 
# row = document_tree.xpath('//*[@id="_market_sum"]')
# 
# print(row)
#===============================================================================

