#-*- coding: utf-8 -*-
'''
Created on 2015. 5. 28.

@author: Jay
'''
from datetime import datetime, time

class stringController():
    '''
    classdocs
    '''

    @staticmethod
    def makeQuotation(str):
        return "'" + str + "'"
    
    @staticmethod
    def cleanUpString(str):
        
        str = str.strip()        
        str = str.replace(',', '')        
        str = str.replace('%', '')
        str = str.replace(unicode('원','utf-8'),'')
        
        return str 
    
    @staticmethod
    def todayDate():
        d = datetime.today()
        return d.strftime("%Y%m%d")
    
    @staticmethod
    def todayTime():
        d = datetime.today()
        return d.strftime("%H%M")
    
    @staticmethod
    def comma():
        return ","