'''
Created on 2015. 6. 2.

@author: Jay
'''
from util.dbConnector import dbConnector
from util.sqlMap import sqlMap
from util.htmlParser import htmlParser

dbInstance = dbConnector(sqlMap.connectInfo)

selectInfo = dbInstance.select(sqlMap.selectStockListUpdate)
stockListMax = dbInstance.select(sqlMap.selectStockListMAX)

for x in selectInfo:
    print(x)
    
for y in stockListMax:
    print(y)

    
for marketIndex in range(0, len(stockListMax)):
    
    urlForMax = stockListMax[marketIndex][3] + repr(1)
    xPathForMax = stockListMax[marketIndex][1]

    maxIndex = htmlParser.xPathParse(urlForMax, xPathForMax)[0][39:]
    
    for pageIndex in range(1, int(maxIndex)):
    
        url = selectInfo[marketIndex][3] + repr(pageIndex)
        xPath = selectInfo[marketIndex][1]

        result = htmlParser.xPathParse(url, xPath)

        for y in result:             
            market = selectInfo[marketIndex][5]
            ticker = y[20:]
            code = market + ticker            
            print(code + " " + market + " " + ticker)
    
        print("=============================================" + repr(pageIndex))
        
    print("+_+_+_+_+_+_+_+_+_+_+_+_+_+__+_+_+_+_+_+")
        
        