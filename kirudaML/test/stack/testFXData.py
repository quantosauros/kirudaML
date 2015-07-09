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
fxCode = ('FX_USDKRW', 'FX_EURKRW', 'FX_JPYKRW', 'FX_CNYKRW', 'FX_GBPKRW', 'FX_CADKRW', 'FX_AUDKRW',)

for fxIndex in range(0, len(fxCode)):
    for pageIndex in range(200, 280):
        
        page = repr(pageIndex)
        url = 'http://info.finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=' + \
            fxCode[fxIndex] + '&page=' + page
        xPath = '/html/body/div/table/tbody/tr/td[2]/text() | /html/body/div/table/tbody/tr/td[1]/text()'    
        #print(url)
        
        result = htmlParser.xPathParse(url, xPath)
        
        #print(result)
        resultLen = len(result)
        
        valueStatement = ""
        for index in range(0, resultLen, 2):    
            date = result[index].replace('.', '')
            value = result[index + 1].replace(',','')
            #print fxCode[fxIndex], date, value
            
            tmpStatement = SC.makeQuotation(fxCode[fxIndex]) + SC.comma() + \
                SC.makeQuotation(date) + SC.comma() + \
                SC.makeQuotation(value)
                
            valueStatement = valueStatement + SC.makeParentheses(tmpStatement) + SC.comma()
                
        
        statement = "INSERT INTO fx_data (code, date, fxRate) VALUES " + valueStatement[:-1]
        
        print(statement)
        #dbInstance.insert(statement)
        #('FX_USDKRW', '20150630', '1114.90');



