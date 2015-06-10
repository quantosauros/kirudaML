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
    
    additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
    url = db_selectParsingInfo[0][1] + db_stockCode[stockIndex][1] + additionalURL
    xPath = db_selectParsingInfo[0][3]
    
    #print(url)
    #print(xPath)
    
    parseResult = htmlParser.xPathParse(url, xPath)
    dataLen = len(parseResult) - len(parseResult)/4 
    
    #print(dataLen)
    TABLENAME = "stock_supdmd"
    COLUMNNAME = "code,date, " if dataLen is not 0 else "code,date" 
    VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
                SC.makeQuotation(SC.todayDate())
    VALUES = VALUES + SC.comma() if dataLen is not 0 else VALUES
                
    #print(db_stockCode[stockIndex])
    for dataIndex in range(0, dataLen):
        comma = "" if dataIndex == dataLen - 1 else SC.comma()
        COLUMNNAME = COLUMNNAME + db_selectParsingInfo[dataIndex][0] + comma
                    
        value = SC.cleanUpString(parseResult[db_selectParsingInfo[dataIndex][4]]).encode('utf8')
                
        if dataIndex % 3 == 0:
            flag = True
            #print(repr(dataIndex) +": "+ value)
            for traderIndex in range(0, traderLen):
                if db_traderInfo[traderIndex][1] == value:
                    value = db_traderInfo[traderIndex][0]
                    #print(value)
                    flag = False
                    break
            if flag == True :
                print(value)
        #print(repr(dataIndex) + ": " + value)    
        VALUES = VALUES + SC.makeQuotation(value) + comma
        
    #print (COLUMNNAME)
    #print(VALUES)
    dbInsertStatement = sqlMap.insertStockData %(TABLENAME, COLUMNNAME, VALUES)
    #print(dbInsertStatement)
    dbInstance.insert(dbInsertStatement)
     
end_time = time.time()
print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")   