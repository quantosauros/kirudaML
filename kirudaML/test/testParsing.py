# -*- coding: cp949 -*-
'''
Created on 2015. 5. 12.

@author: Jay
'''

from bs4 import BeautifulSoup
import urllib2
from util import htmlParser
#from test.HTMLParse import HTMLParse

url = 'http://finance.naver.com/item/sise.nhn?code=008770'
regularExp1 = ["span", "tah p11 nv01"]
regularExp2 = ["span", "tah p11 red01"]
 
result1 = htmlParser.htmlParser.parse1(url, regularExp1)
i = 0
for x in result1:
    print("%d : " % i)
    print(x.text)
    i = i + 1
    
result2 = htmlParser.htmlParser.parse1(url, regularExp2)
i = 0
for x in result2:
    print("%d : " % i)
    print(x.text)
    i = i + 1



#=============================================================================== 
# # NAVER 시세
# url = 'http://finance.naver.com/item/sise.nhn?code=008770'
# regularExp = ["table", "type2 type_tax", "td"]
# 
# result1 = htmlParser.htmlParser.parse(url, regularExp)
# i = 0
# for x in result1:
#     print("%d : " % i)
#     print(x.text)
#     i = i + 1
#===============================================================================

#===============================================================================
# 
# # Naver 주식종목
# url = "http://finance.naver.com/item/main.nhn?code=008770"
# # 투자정보
# regularExp1 = ["div", "tab_con1", "em"]
# # 호가 10단계
# reqularExp2= ["div", "tab_con2", "td"]
# 
# result1 = htmlParser.htmlParser.parse(url, regularExp1);
# # 0 : 시가총액
# # 1 : 시가총액순위
# # 2 : 상장주식수
# # 3 : 액면가
# # 4 : 매매단위
# # 5 : 외국인한도주식수
# # 6 : 외국인보유주식수
# # 7 : 외국인소진율
# # 8 : 투자의견
# # 9 : 목표주가
# # 10 : 52주최고
# # 11 : 52주최저
# # 12 : PER
# # 13 : EPS
# # 14 : PBR
# # 15 : BPS
# # 16 : 추정PER
# # 17 : EPS
# # 18 : 부채비율
# # 19 : 동일업종PER
# # 20 : 동일업종 등략률
# i = 0
# for x in result1:
#     print("%d : " % i)
#     print(x.text)
#     i = i + 1
# 
# page = urllib2.urlopen(url)
# soup = BeautifulSoup(page, from_encoding="euc-kr")
#===============================================================================
