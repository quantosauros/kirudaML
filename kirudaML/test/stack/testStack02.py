#-*- coding: utf-8 -*-
'''
Created on 2015. 5. 15.

@author: Jay
'''
from util.sqlMap import sqlMap
from util.dbConnector import dbConnector
from util.htmlParser import htmlParser
from util.stringController import stringController as SC
  

dbInstance = dbConnector(sqlMap.connectInfo)

stockCode = dbInstance.select(sqlMap.selectStockCode)
selectInfo = dbInstance.select(sqlMap.selectStockInfoDaily)

#print(stockCode)
#print(selectInfo)

dataIndex = 0
stockIndex = 0

resultArray = {}

for stockIndex in range(0, len(stockCode)):
    tmpResult = {}
    for dataIndex in range(0, len(selectInfo)):        
        #print(dataIndex, stockIndex)
        url = selectInfo[dataIndex][3] + stockCode[stockIndex][2] + selectInfo[dataIndex][4]
        xPath = selectInfo[dataIndex][1]
                
        result1 = htmlParser.xPathParse(url, xPath)        
        
        value = SC.cleanUpString(result1[selectInfo[dataIndex][2]])
        #newValue = value.replace(',', '').replace('%', '')
        
        #print(stockCode[stockIndex][0]+ "("+ selectInfo[dataIndex][5] +")  : " + value)
        
        tmpResult[selectInfo[dataIndex][5]] = value
        
    resultArray[stockIndex] = tmpResult


TABLENAME = "stock_sisae"

for stockIndex in range(0,len(resultArray)):
    result = resultArray[stockIndex]
    COLUMNNAME = "code,date,"
     
    VALUES = SC.makeQuotation(stockCode[stockIndex][0]) + SC.comma() + \
            SC.makeQuotation(SC.todayDate()) + SC.comma()
    
    for dataIndex in range(0, len(selectInfo)):        
        comma = "" if dataIndex == len(selectInfo) - 1 else SC.comma()
        
        COLUMNNAME = COLUMNNAME + selectInfo[dataIndex][5] + comma
        #print(COLUMNNAME)
        
        VALUES = VALUES + SC.makeQuotation(str(result[selectInfo[dataIndex][5]])) + comma
            #SC.makeQuotation(str(result['netChange'])) + SC.comma() + \
            #SC.makeQuotation(str(result['priceChange']))
        #print(VALUES)
        
        
    dbInsertStatement = sqlMap.insertStockData %(TABLENAME, COLUMNNAME, VALUES)
    print(dbInsertStatement)
    dbInstance.insert(dbInsertStatement)
    

