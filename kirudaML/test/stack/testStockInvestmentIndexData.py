#-*- coding: utf-8 -*-
'''
Created on 2015. 6. 20.

@author: Jay
'''
from util.dbConnector import dbConnector
from util.sqlMap import sqlMap
from lxml import html
from util.stringController import stringController as SC


dbInstance = dbConnector(sqlMap.connectInfo)
db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_krx_investmentIndex'))

#print(db_selectParsingInfo)


TABLENAME = "stock_sisae_test"
COLUMNNAME = "(code,date,designated, EPS,PER,BPS,PBR,dividendAmount, dividendPercent)"
marketGubun = ('2','3')
marketCode = ('KS','KQ')
date = '20150619'
additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
url = db_selectParsingInfo[0][1]
xPath = db_selectParsingInfo[0][3]    
increment = 13

for marketIndex in range(0, len(marketGubun)):
    
    #code = db_stockCode[marketIndex][0]
    #date = SC.todayDate()
    
    fr_work_dt = date
    to_work_dt = date

    parameters = '&market=' + \
        '&CMD=' + \
        '&cur_page=1' + \
        '&pageSize=3000' + \
        '&market_gubun=' + marketGubun[marketIndex] +\
        '&gubun=1' + \
        '&mthd=' + \
        '&fr_work_dt=' + fr_work_dt +\
        '&to_work_dt=' + to_work_dt +\
        '&searchBtn=' + \
        '&searchBtn2=%EC%A1%B0%ED%9A%8C'   
        
    htm = html.parse(url + parameters)
    result = htm.xpath(xPath)
    #print(result)
    
    VALUERESULT = ""
    for dd in range(0, len(result), increment):
        code = marketCode[marketIndex] + result[1 + dd]
        VALUES = SC.makeQuotation(code) + SC.comma() + \
            SC.makeQuotation(date) + SC.comma()
          
        for index in range(0, len(db_selectParsingInfo)):
            variable = db_selectParsingInfo[index][0]
            vIndex = db_selectParsingInfo[index][4] + dd
            value = SC.cleanUpString(result[vIndex]).encode('utf8')
            #print(variable, vIndex, value)
            if variable == 'designated':
                value = 'Y' if value == '관리종목' else 'N'                 
            if variable == 'PER' and value == '-':
                value = '0'
            if variable == 'BPS' and value == '-':
                value = '0'
            if variable == 'PBR' and value == '-':
                value = '0'
            if value == '':
                value = '0'
            
            
            VALUES = VALUES + SC.makeQuotation(value) + SC.comma()
            
        VALUERESULT = VALUERESULT + SC.makeParentheses(VALUES[:-1]) + SC.comma()
        
    #print(VALUERESULT)
    dbInsertStatement = sqlMap.INSERTINVESTINDEXDATA %(VALUERESULT[:-1])
    #print(dbInsertStatement)
    #dbInstance.insert(dbInsertStatement)
     
    
