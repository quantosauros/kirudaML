#-*- coding: utf-8 -*-
'''
Created on 2015. 5. 14.

@author: Jay
'''
from datetime import datetime
import time

from util.dbConnector import dbConnector
from util.htmlParser import htmlParser
from util.sqlMap import sqlMap
from util.stringController import stringController as SC


class stackData:
    '''
    classdocs
    '''
    @staticmethod
    def StockDailyData():
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
                dbInstance.insert(dbInsertStatement)
                
        
        
        end_time = time.time()
        print("Stack the Daily Stock Data at " + SC.todayDate() + SC.todayTime())
        print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")

    