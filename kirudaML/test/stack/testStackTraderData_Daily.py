#-*- coding: utf-8 -*-
'''
Created on 2015. 6. 9.

@author: Jay
'''
from util.dbConnector import dbConnector
from util.sqlMap import sqlMap
from util.htmlParser import htmlParser
from util.stringController import stringController as SC
import time

start_time = time.time()

dbInstance = dbConnector(sqlMap.connectInfo)
db_stockCode = dbInstance.select(sqlMap.selectStockCode)
db_selectParsingInfo = dbInstance.select(sqlMap.SELECTTRADERINFO_XPATH)
db_traderInfo = dbInstance.select(sqlMap.SELECTTRADERINFO)
#print(db_stockCode)
#print(db_selectParsingInfo)
#print(db_traderInfo)

stockLen = len(db_stockCode)
traderLen = len(db_traderInfo)

for stockIndex in range(0, stockLen):
    
    #additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
    additionalURL = "&beforeday=1"
    url = db_selectParsingInfo[0][1] + db_stockCode[stockIndex][1] + additionalURL
    xPath = db_selectParsingInfo[0][3]
    
    #print(url)
    #print(xPath)
    
    parseResult = htmlParser.xPathParse(url, xPath)
    dataLen = len(parseResult) - len(parseResult)/4 
    
    if dataLen is 0:
        continue
    
    #print(dataLen)
    TABLENAME = "stock_trader"
    COLUMNNAME = "(code,date,traderCode,buyVolume,sellVolume)"
        
    
    #VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
    #            SC.makeQuotation(SC.todayDate())
    #VALUES = VALUES + SC.comma() if dataLen is not 0 else VALUES
    
    tmpData = {};   
    #print(db_stockCode[stockIndex])
    for dataIndex in range(0, dataLen, 3):
        #comma = "" if dataIndex == dataLen - 1 else SC.comma()
        #COLUMNNAME = COLUMNNAME + db_selectParsingInfo[dataIndex][0] + comma
        
        traderNameIndex = db_selectParsingInfo[dataIndex][4]
        buyVolIndex = db_selectParsingInfo[dataIndex + 1][4]
        sellVolIndex = db_selectParsingInfo[dataIndex + 2][4]
        
        traderName = SC.cleanUpString(parseResult[traderNameIndex]).encode('utf8')
        buyVol = SC.cleanUpString(parseResult[buyVolIndex]).encode('utf8')
        sellVol = SC.cleanUpString(parseResult[sellVolIndex]).encode('utf8')
        
        #print(repr(dataIndex) +": "+ traderName)
        #print(repr(dataIndex) +": "+ buyVol)
        #print(repr(dataIndex) +": "+ sellVol)
        
        flag = True
        for traderIndex in range(0, traderLen):
            if db_traderInfo[traderIndex][1] == traderName:
                traderName = db_traderInfo[traderIndex][0]
                #print(traderName)
                flag = False
                break
        if flag == True :
            print(traderName)
        #print(repr(dataIndex) + ": " + traderName)    
        #VALUES = VALUES + SC.makeQuotation(traderName) + comma
        tmpData[traderName] = (buyVol, sellVol)
        #print(tmpData)
    
    VALUERESULT = ""
    
    for data in tmpData:
        
        traderName = data
        buyVol = tmpData[data][0]
        sellVol = tmpData[data][1]
        
        VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
            SC.makeQuotation(SC.todayDate()) + SC.comma() + \
            SC.makeQuotation(traderName) + SC.comma() + \
            SC.makeQuotation(buyVol) + SC.comma() + \
            SC.makeQuotation(sellVol)
        
        VALUERESULT = VALUERESULT + SC.makeParentheses(VALUES) + SC.comma()
        #print(VALUES)
    dbInsertStatement = sqlMap.INSERTDATAWITHOUTPARENTHESES %(TABLENAME, COLUMNNAME, VALUERESULT[:-1])
    print(dbInsertStatement)
    dbInstance.insert(dbInsertStatement)
        
    #print (COLUMNNAME)
    #print(VALUES)
        
    
     
end_time = time.time()
print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")   