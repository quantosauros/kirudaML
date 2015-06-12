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
        #null인 경우 quotation 없이 return
        if "null" in str:
            return str;
        else :
            return "'" + str + "'"
    
    @staticmethod
    def cleanUpString(str):        
        str = str.strip()        
        str = str.replace(',', '')        
        str = str.replace('%', '')
        str = str.replace('/', '')
        str = str.replace(unicode('원','utf-8'),'')
        #값이 N/A인 경우, null로 입력
        if "N/A" in str :
            str = 'null'
            return str
                 
        return str


    @staticmethod
    def cleanUpStringForFaceValue(str):
        tmp = str.split()
        if len(tmp) is not 1:
            return tmp[0]
        else: 
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
    
    @staticmethod
    def makeParentheses(str):
        return "(" + str + ")"