# coding: utf-8
'''
Created on 2015. 5. 26.

@author: Jay
'''
from util.sqlMap import sqlMap
from util.dbConnector import dbConnector
from util.htmlParser import htmlParser

dbInstance = dbConnector(sqlMap.connectInfo)

stockCode = dbInstance.select(sqlMap.selectStockCode)
selectInfo = dbInstance.select(sqlMap.selectStockInfo)

#===============================================================================
# for x in stockCode:
#     print(x)
# for y in selectInfo:
#     print(y)
#===============================================================================

#dataIndex = 0
#stockIndex = 0

for stockIndex in range(0, len(stockCode)):
    for dataIndex in range(0, len(selectInfo)):
        
        url = selectInfo[dataIndex][3] + stockCode[stockIndex][2] + selectInfo[dataIndex][4]
        xPath = selectInfo[dataIndex][1]       
        
        result1 = htmlParser.xPathParse(url, xPath)        
        value = result1[selectInfo[dataIndex][2]].strip().replace(',','').replace('%','').replace(unicode('원','utf-8'),'')
        
        #print(stockIndex,dataIndex)
        #print("dataName: " + selectInfo[dataIndex][5])
        #print("xPath: " + xPath)
        #print("url: " + url)      
        #print("index: "+ str(selectInfo[dataIndex][2]))
        #print(value)
        print(stockCode[stockIndex][0]+ "("+ selectInfo[dataIndex][5] +")  : " + value)




