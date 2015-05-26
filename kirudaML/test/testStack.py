#-*- coding: utf-8 -*-
'''
Created on 2015. 5. 15.

@author: Jay
'''
from util.sqlMap import sqlMap
from util.dbConnector import dbConnector
from util.htmlParser import htmlParser

dbInstance = dbConnector(sqlMap.connectInfo)

stockCode = dbInstance.select(sqlMap.selectStockCode)
selectInfo = dbInstance.select(sqlMap.selectStockInfo)

print(stockCode)
print(selectInfo)

dataIndex = 0
stockIndex = 0

for stockIndex in range(0, len(stockCode)):
    for dataIndex in range(0, len(selectInfo)):        
        #print(dataIndex, stockIndex)
        url = selectInfo[dataIndex][6] + stockCode[stockIndex][2]        
        result1 = htmlParser.parse(url, (selectInfo[dataIndex][1], selectInfo[dataIndex][2], selectInfo[dataIndex][3]));
        #print(result1)
        #result2 = dbInstance.select(sqlMap.selectDataInfo %(selectInfo[dataIndex][9], selectInfo[dataIndex][8]))
        value = result1[selectInfo[dataIndex][5]].text.replace(',', '').replace('%', '');
        #newValue = value.replace(',', '').replace('%', '')
        newValue = float(value)# * int(result2[0][1])
        print(stockCode[stockIndex][3]+ "("+ selectInfo[dataIndex][8] +")  : " + str(newValue))