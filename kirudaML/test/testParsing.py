# -*- coding: cp949 -*-
'''
Created on 2015. 5. 12.

@author: Jay
'''

from bs4 import BeautifulSoup
import urllib2
from util import htmlParser
#from test.HTMLParse import HTMLParse


# Naver �ֽ�����
url = "http://finance.naver.com/item/main.nhn?code=008770"
# ��������
regularExp1 = ["div", "tab_con1", "em"]
# ȣ�� 10�ܰ�
reqularExp2= ["div", "tab_con2", "td"]

result1 = htmlParser.htmlParser.parse(url, regularExp1);
# 0 : �ð��Ѿ�
# 1 : �ð��Ѿ׼���
# 2 : �����ֽļ�
# 3 : �׸鰡
# 4 : �ŸŴ���
# 5 : �ܱ����ѵ��ֽļ�
# 6 : �ܱ��κ����ֽļ�
# 7 : �ܱ��μ�����
# 8 : �����ǰ�
# 9 : ��ǥ�ְ�
# 10 : 52���ְ�
# 11 : 52������
# 12 : PER
# 13 : EPS
# 14 : PBR
# 15 : BPS
# 16 : ����PER
# 17 : EPS
# 18 : ��ä����
# 19 : ���Ͼ���PER
# 20 : ���Ͼ��� ���
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

