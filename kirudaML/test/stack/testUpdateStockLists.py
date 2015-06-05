'''
Created on 2015. 6. 2.

@author: Jay
'''
from util.dbConnector import dbConnector
from util.sqlMap import sqlMap
from util.htmlParser import htmlParser
from util.stringController import stringController as SC

dbInstance = dbConnector(sqlMap.connectInfo)
db_selectSiteData_XPath = dbInstance.select(sqlMap.SELECTSITEDATA_XPATH %('L'))
db_listInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %(db_selectSiteData_XPath[0]))
db_maxInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %(db_selectSiteData_XPath[1]))

for marketIndex in range(0, len(db_listInfo)):
     
    urlForMax = db_maxInfo[marketIndex][1] + repr(1)
    xPathForMax = db_maxInfo[marketIndex][3] 
    maxIndex = htmlParser.xPathParse(urlForMax, xPathForMax)[0][39:]
     
    market = db_listInfo[marketIndex][0]
    
    values = "("
    for pageIndex in range(1, int(maxIndex)):
     
        url = db_listInfo[marketIndex][1] + repr(pageIndex)
        xPath = db_listInfo[marketIndex][3] 
        result = htmlParser.xPathParse(url, xPath)
 
        for y in result:
            #lastStr = ", \n (" if pageIndex != int(maxIndex) - 1 else ""
            
            ticker = y[20:]
            code = market + ticker
            #print(code + "," + ticker + "," + market)
            
            values = values + \
                SC.makeQuotation(code) + SC.comma() + \
                SC.makeQuotation(ticker) + SC.comma() + \
                SC.makeQuotation(market) + SC.comma() + \
                "NOW()), \n ("
    
    query = sqlMap.insertStockList %(values[:-5])         
    #print(query)
    
    dbInstance.insert(query)
       
        
#==============================================================================
#          
# val = "'KQ000250', '000250', 'KQ'"
# 
# query = sqlMap.insertStockList %(val)
# 
# print(query)
# 
# dbInstance.insert(query)
#===============================================================================

 