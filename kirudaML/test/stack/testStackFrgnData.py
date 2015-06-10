'''
Created on 2015. 6. 10.

@author: Jay
'''
import time
from util.dbConnector import dbConnector
from util.sqlMap import sqlMap
from util.htmlParser import htmlParser
from util.stringController import stringController as SC

start_time = time.time()

dbInstance = dbConnector(sqlMap.connectInfo)
db_stockCode = dbInstance.select(sqlMap.selectStockCode)
db_selectParsingInfo = dbInstance.select(sqlMap.SELECTFRGNINFO_XPATH)

#print(db_selectParsingInfo)

stockLen = len(db_stockCode)

for stockIndex in range(0, stockLen):
    
    additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
    url = db_selectParsingInfo[0][1] + db_stockCode[stockIndex][1] + additionalURL
    xPath = db_selectParsingInfo[0][3]
    
    parseResult = htmlParser.xPathParse(url, xPath)
        
    dataLen = len(db_selectParsingInfo)    
    TABLENAME = "stock_supdmd"
    COLUMNNAME = "code,date, " if dataLen is not 0 else "code,date"
    VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
        SC.makeQuotation(SC.todayDate())
        
    VALUES = VALUES + SC.comma() if dataLen is not 0 else VALUES

    for dataIndex in range(0, dataLen):
        
        comma = "" if dataIndex == dataLen - 1 else SC.comma()        
        COLUMNNAME = COLUMNNAME + db_selectParsingInfo[dataIndex][0] + comma
        
        value = SC.cleanUpString(parseResult[db_selectParsingInfo[dataIndex][4]]).encode('utf8')        
        VALUES = VALUES + SC.makeQuotation(value) + comma
        #print(value)
        
    dbInsertStatement = sqlMap.INSERTFRGNDATA %(VALUES)
    print(dbInsertStatement)
    dbInstance.insert(dbInsertStatement)
        
        
end_time = time.time()
print("Stack the Foreign and Institution Data at " + SC.todayDate() + SC.todayTime())
print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")   



        