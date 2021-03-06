'''
Created on 2015. 5. 12.

@author: Jay
'''
import urllib2
from bs4 import BeautifulSoup
from lxml import html

class htmlParser:
        
    @staticmethod
    def parse(url, regularExp):
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, from_encoding="euc-kr")
        str = soup.find_all(regularExp[0], regularExp[1])[0].find_all(regularExp[2])
        return str

    @staticmethod
    def xPathParse(url, xPath, encodingMethod = 'utf-8'):
        parser1 = html.HTMLParser(encoding = encodingMethod)
        htm = html.parse(url, parser = parser1)                
        result = htm.xpath(xPath)
        return result