#-*- coding: utf-8 -*-
'''
Created on 2015. 6. 30.

@author: Jay
'''
from util.htmlParser import htmlParser
from util.stringController import stringController as SC
from util.dbConnector import dbConnector
from util.sqlMap import sqlMap

dbInstance = dbConnector(sqlMap.connectInfo)
fxCode = ('OIL_CL','OIL_DU','OIL_BRT','CMDT_GC')
#300, 323, 303, 299
for fxIndex in range(0, len(fxCode)):
    for pageIndex in range(307, 323):
        
        page = repr(pageIndex)
        url = 'http://info.finance.naver.com/marketindex/worldDailyQuote.nhn?marketindexCd=' +\
                fxCode[fxIndex] + '&fdtc=2' + \
                '&page=' + page
        xPath = '/html/body/div/table/tbody/tr/td[1]/text() | /html/body/div/table/tbody/tr/td[2]/text()'    
        #print(url)
        
        result = htmlParser.xPathParse(url, xPath)
        
        #print(result)
        resultLen = len(result)
        
        valueStatement = ""
        for index in range(0, resultLen, 2):    
            date = SC.cleanUpString(result[index].replace('.', ''))
            value = SC.cleanUpString(result[index + 1].replace(',',''))
            #print fxCode[fxIndex], date, value
            
            tmpStatement = SC.makeQuotation(fxCode[fxIndex]) + SC.comma() + \
                SC.makeQuotation(date) + SC.comma() + \
                SC.makeQuotation(value)
                
            valueStatement = valueStatement + SC.makeParentheses(tmpStatement) + SC.comma()
                
        
        statement = "INSERT INTO fx_data (code, date, fxRate) VALUES " + valueStatement[:-1]
        
        print(statement)
        dbInstance.insert(statement)
        



