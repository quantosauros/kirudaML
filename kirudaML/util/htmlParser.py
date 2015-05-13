'''
Created on 2015. 5. 12.

@author: Jay
'''
import urllib2
from bs4 import BeautifulSoup

class htmlParser:
        
    @staticmethod
    def parse(url, regularExp):
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, from_encoding="euc-kr")
        str = soup.find_all(regularExp[0], regularExp[1])[0].find_all(regularExp[2])
        return str;