#-*- coding: utf-8 -*-
'''
Created on 2015. 5. 14.

@author: Jay
'''
import time
from util.dbConnector import dbConnector
from util.htmlParser import htmlParser
from util.sqlMap import sqlMap
from util.stringController import stringController as SC
from util.config import config

class stackData:
    '''
    classdocs
    '''
    @staticmethod
    def StockSisaeData():
        start_time = time.time()
        f = open(config.logPath + config.logName_StockSisaeData, 'w')

        dbInstance = dbConnector(sqlMap.connectInfo)
        db_stockCode = dbInstance.select(sqlMap.selectStockCode)
        #db_selectSiteData_XPath = dbInstance.select(sqlMap.SELECTSITEDATA_XPATH %('D'))

        #parseIndex = 0
        #stockIndex = 0
        #dataIndex = 0
        TABLENAME = "stock_sisae"
        #print(db_selectSiteData_XPath)
        
        #for parseIndex in range(0, len(db_selectSiteData_XPath)):
        db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_na_sisae01'))
        print(db_selectParsingInfo)

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

            #빈 데이터가 있을 경우(Face Value가 없음) 0으로 예외처리
            if len(parseResult) is not len(db_selectParsingInfo):
                parseResult.insert(10, '0')
                
            for dataIndex in range(0, len(db_selectParsingInfo)):                                                   
                comma = "" if dataIndex == len(parseResult) - 1 else SC.comma()            
                COLUMNNAME = COLUMNNAME + db_selectParsingInfo[dataIndex][0] + comma            
                value = SC.cleanUpString(parseResult[db_selectParsingInfo[dataIndex][4]])
                                    
                #액면가가 국외통화인 경우, 통화코드 제거
                if db_selectParsingInfo[dataIndex][0] == 'faceValue':
                    value = SC.cleanUpStringForFaceValue(value)
                    
                VALUES = VALUES + SC.makeQuotation(value) + comma                        
                #print(db_selectParsingInfo[dataIndex][0] + ": " + SC.cleanUpString(value))
        
            #print(COLUMNNAME)
            #print(VALUES)     
            dbInsertStatement = sqlMap.insertStockData %(TABLENAME, COLUMNNAME, VALUES)
            print(dbInsertStatement)
            f.write(dbInsertStatement)
            dbInstance.insert(dbInsertStatement)        
    
        end_time = time.time()
        print("Stack the Daily Stock Data at " + SC.todayDate() + SC.todayTime())
        print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
        
        f.write("Stack the Daily Stock Data at " + SC.todayDate() + SC.todayTime())
        f.write("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
        f.close()

    @staticmethod
    def UpdateStockLists():
        
        f = open(config.logPath + config.logName_UpdateStockLists, 'w')
        
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
            for pageIndex in range(1, int(maxIndex) + 1):
                
                url = db_listInfo[marketIndex][1] + repr(pageIndex)
                xPath = db_listInfo[marketIndex][3] 
                result = htmlParser.xPathParse(url, xPath)
                
                for y in result:             
                    
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
            f.write(query)
            dbInstance.insert(query)
        
        f.close()
           
    @staticmethod
    def StockTraderData():
        start_time = time.time()
        
        dbInstance = dbConnector(sqlMap.connectInfo)
        db_stockCode = dbInstance.select(sqlMap.selectStockCode)
        db_selectParsingInfo = dbInstance.select(sqlMap.SELECTTRADERINFO_XPATH)
        
        stockLen = len(db_stockCode)
        
        for stockIndex in range(0, stockLen):
            
            additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
            url = db_selectParsingInfo[0][1] + db_stockCode[stockIndex][1] + additionalURL
            xPath = db_selectParsingInfo[0][3]
            
            parseResult = htmlParser.xPathParse(url, xPath)
            dataLen = len(parseResult) - len(parseResult)/4
            
            TABLENAME = "stock_supdmd"
            COLUMNNAME = "code,date,"
            VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
                SC.makeQuotation(SC.todayDate()) + SC.comma()
                
            for dataIndex in range(0, dataLen):
                
                comma = "" if dataIndex == dataLen - 1 else SC.comma()
                COLUMNNAME = COLUMNNAME + db_selectParsingInfo[dataIndex][0] + comma
        
                value = SC.cleanUpString(parseResult[db_selectParsingInfo[dataIndex][4]])
                #print(repr(dataIndex) + ": " + value)    
                VALUES = VALUES + SC.makeQuotation(value) + comma
                
            #print (COLUMNNAME)
            #print(VALUES)
            dbInsertStatement = sqlMap.insertStockData %(TABLENAME, COLUMNNAME, VALUES)
            #dbInstance.insert(dbInsertStatement)
            print(dbInsertStatement)
            
        end_time = time.time()
        print("Stack the Trader Data at " + SC.todayDate() + SC.todayTime())
        print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
        
                    