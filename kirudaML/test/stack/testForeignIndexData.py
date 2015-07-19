'''
Created on 2015. 7. 17.

@author: Jay
'''
from util.htmlParser import htmlParser
from lxml import html
import json
from util.stringController import stringController as SC
from util.dbConnector import dbConnector
from util.sqlMap import sqlMap

dbInstance = dbConnector(sqlMap.connectInfo)
#===============================================================================
# symbols = ('DJI@DJI','DJI@DJT','NAS@IXIC','NAS@NDX','NAS@SOX',
#            'SHS@000001','SHS@000002','SHS@000003', 
#            'NII@NI225',
#            'HSI@HSI', 'HSI@HSCE', 'HSI@HSCC', 
#            'LNS@FTSE100', 'PAS@CAC40', 'XTR@DAX30')
#===============================================================================
symbols = ('LNS@FTSE100',)
endPage = 342
startSymbol = 0
endSymbol = len(symbols)
for symbolIndex in range(startSymbol, endSymbol) :
    for pageIndex in range(1, endPage) :
        url = 'http://finance.naver.com/world/worldDayListJson.nhn?symbol=' + symbols[symbolIndex] + '&fdtc=0&page=' + repr(pageIndex)
        xPath = '*//text()'
        #xPath = '/html/body/div/table/tbody/tr/td/text()'
            
        #print(url)
        parser1 = html.HTMLParser(encoding = 'utf-8')
        htm = html.parse(url, parser = parser1)   
                     
        result = htm.xpath(xPath)
        #print result
        str = result[0][1:-2]
        splitedString = str.split('},')
        
        valueStatement = ""
        for x in splitedString :
            tmpStr = x + '}'
            #print tmpStr
            data = json.loads(tmpStr)
            #print data
            
            code = symbols[symbolIndex]
            date = data['xymd'] 
            close = repr(data['clos']) 
            open = data['open']
            high = data['high'] 
            low = data['low']
            
            #print date, close, open, high, low
            tmpStatement = SC.makeQuotation(code) + SC.comma() + \
                SC.makeQuotation(date) + SC.comma() + \
                SC.makeQuotation(close)
                
            valueStatement = valueStatement + SC.makeParentheses(tmpStatement) + SC.comma()
            
        statement = "INSERT INTO index_data (code, date, value) VALUES " + valueStatement[:-1]
        print statement
        dbInstance.insert(statement)
    
    