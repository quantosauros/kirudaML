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
indexCode = ('KPI200',)#'KOSPI','KOSDAQ','KPI200',)
#'DJI@DJI','DJI@DJT','NAS@IXIC','NAS@NDX','NAS@SOX','SHS@000001',)
#1120, 801, 393
for idIndex in range(0, len(indexCode)):
    for pageIndex in range(1, 394):
        
        page = repr(pageIndex)
        url = 'http://finance.naver.com/sise/sise_index_day.nhn?code=' + \
            indexCode[idIndex] + '&page=' + page
        xPath = '*//*[contains(@class, "date")]/text() | *//*[contains(@class, "number")]/text()'
        #xPath = '/html/body/div/table/tbody/tr/td/text()'
            
        #print(url)
        
        result = htmlParser.xPathParse(url, xPath)
        
        #print(result)
        resultLen = len(result)
        
        valueStatement = ""
        for index in range(0, resultLen, 6):    
            date = result[index].replace('.', '')
            value = result[index + 1].replace(',','')
            #print indexCode[idIndex], date, value
            
            tmpStatement = SC.makeQuotation(indexCode[idIndex]) + SC.comma() + \
                SC.makeQuotation(date) + SC.comma() + \
                SC.makeQuotation(value)
                
            valueStatement = valueStatement + SC.makeParentheses(tmpStatement) + SC.comma()
                
        
        statement = "INSERT INTO index_data (code, date, value) VALUES " + valueStatement[:-1]
        
        print(statement)
        dbInstance.insert(statement)
        #('FX_USDKRW', '20150630', '1114.90');



