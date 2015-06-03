#-*- coding: utf-8 -*-
'''
Created on 2015. 5. 15.

@author: Jay
'''
import time
from util.dbConnector import dbConnector
from util.htmlParser import htmlParser
from util.sqlMap import sqlMap
from util.stringController import stringController as SC


start_time = time.time()

dbInstance = dbConnector(sqlMap.connectInfo)
db_stockCode = dbInstance.select(sqlMap.selectStockCode)
db_selectSiteData_XPath = dbInstance.select(sqlMap.SELECTSITEDATA_XPATH %('D'))

#parseIndex = 0
#stockIndex = 0
#dataIndex = 0
TABLENAME = "stock_sisae"

for parseIndex in range(0, len(db_selectSiteData_XPath)):
    db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %(db_selectSiteData_XPath[parseIndex]))
    #print(db_selectParsingInfo)
    
    for stockIndex in range(0, len(db_stockCode)):
        #print(repr(stockIndex) +" : " + db_stockCode[stockIndex][0])
        url = db_selectParsingInfo[0][1] + db_stockCode[stockIndex][1] + db_selectParsingInfo[0][2]
        xPath = db_selectParsingInfo[0][3]    
        #print(url)
        #print(xPath)
    
        parseResult = htmlParser.xPathParse(url, xPath)    
        #print(parseResult)
        
        COLUMNNAME = "code,date,"
        VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
            SC.makeQuotation(SC.todayDate()) + SC.comma()
                    
        for dataIndex in range(0, len(parseResult)):
            comma = "" if dataIndex == len(parseResult) - 1 else SC.comma()
            
            COLUMNNAME = COLUMNNAME + db_selectParsingInfo[dataIndex][0] + comma            
            value = parseResult[db_selectParsingInfo[dataIndex][4]]
            VALUES = VALUES + SC.makeQuotation(SC.cleanUpString(value)) + comma                        
            #print(db_selectParsingInfo[dataIndex][0] + ": " + SC.cleanUpString(value))
            
        #print(COLUMNNAME)
        #print(VALUES)     
        dbInsertStatement = sqlMap.insertStockData %(TABLENAME, COLUMNNAME, VALUES)
        #dbInstance.insert(dbInsertStatement)
        print(dbInsertStatement)
        
        
end_time = time.time()
print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")

#===============================================================================
# 
# resultArray = {}
# 
# for stockIndex in range(0, len(stockCode)):
#     tmpResult = {}
#     for parseIndex in range(0, len(selectInfo)):        
#         #print(parseIndex, stockIndex)
#         url = selectInfo[parseIndex][3] + stockCode[stockIndex][2] + selectInfo[parseIndex][4]
#         xPath = selectInfo[parseIndex][1]
#                 
#         result1 = htmlParser.xPathParse(url, xPath)        
#         
#         value = SC.cleanUpString(result1[selectInfo[parseIndex][2]])
#         #newValue = value.replace(',', '').replace('%', '')
#         
#         #print(stockCode[stockIndex][0]+ "("+ selectInfo[parseIndex][5] +")  : " + value)
#         
#         tmpResult[selectInfo[parseIndex][5]] = value
#         
#     resultArray[stockIndex] = tmpResult
# 
# 
# TABLENAME = "stock_sisae"
# 
# for stockIndex in range(0,len(resultArray)):
#     result = resultArray[stockIndex]
#     COLUMNNAME = "code,date,"
#      
#     VALUES = SC.makeQuotation(stockCode[stockIndex][0]) + SC.comma() + \
#             SC.makeQuotation(SC.todayDate()) + SC.comma()
#     
#     for parseIndex in range(0, len(selectInfo)):        
#         comma = "" if parseIndex == len(selectInfo) - 1 else SC.comma()
#         
#         COLUMNNAME = COLUMNNAME + selectInfo[parseIndex][5] + comma
#         #print(COLUMNNAME)
#         
#         VALUES = VALUES + SC.makeQuotation(str(result[selectInfo[parseIndex][5]])) + comma
#             #SC.makeQuotation(str(result['netChange'])) + SC.comma() + \
#             #SC.makeQuotation(str(result['priceChange']))
#         #print(VALUES)
#         
#         
#     dbInsertStatement = sqlMap.insertStockData %(TABLENAME, COLUMNNAME, VALUES)
#     print(dbInsertStatement)
#     dbInstance.insert(dbInsertStatement)
#     
#===============================================================================

