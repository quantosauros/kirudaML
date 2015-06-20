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
from lxml import html

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

            #빈 데이터가 있을 경우(Face Value가 없음) 0으로 예외처리
            if len(parseResult) is not len(db_selectParsingInfo):
                parseResult.insert(10, '0')
                
            for dataIndex in range(0, len(db_selectParsingInfo)):                                                   
                comma = "" if dataIndex == len(db_selectParsingInfo) - 1 else SC.comma()            
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
        db_ParsingInfo = dbInstance.select(sqlMap.SELECTSTOCKLISTINFO_XPATH)
        
        #print(db_ParsingInfo)
        
        countryCode = "KR"
        gubuns = ("kospiVal", "kosdaqVal", "konexVal")
        markets = ("KS", "KQ", "KX")
        basetickerIndex = 1
        basenameIndex = 3
        basekrxCodeIndex = 5
        increment = 7
        
        for marketIndex in range(0,2):
    
            url = db_ParsingInfo[0][1] + gubuns[marketIndex]  
            xPath = db_ParsingInfo[0][3]    
            #print(url, xPath)
            
            result = htmlParser.xPathParse(url, xPath)
            totalLen = len(result)
            
            values = "("
            for index in range(0, totalLen, increment):
            
                tickerIndex = index + basetickerIndex
                nameIndex = index + basenameIndex
                krxCodeIndex = index + basekrxCodeIndex
                
                #print(tickerIndex, nameIndex, krxCodeIndex)
                
                ticker = result[tickerIndex][1:]
                name = result[nameIndex].encode('utf8')
                krxCode = result[krxCodeIndex]
                
                market = markets[marketIndex] 
                code = market + ticker
                #print(name)
                
                #print(code + " " + ticker + " " + market + " " + krxCode + " " + name + " " + countryCode)
                values = values + \
                    SC.makeQuotation(code) + SC.comma() + \
                    SC.makeQuotation(ticker) + SC.comma() + \
                    SC.makeQuotation(market) + SC.comma() + \
                    SC.makeQuotation(krxCode) + SC.comma() + \
                    SC.makeQuotation(name) + SC.comma() + \
                    SC.makeQuotation(countryCode) + SC.comma() + \
                    "NOW()), \n ("
                    
                #print(values)
                
            query = sqlMap.INSERTSTOCKLIST %(values[:-5])    
            print(query)
            dbInstance.insert(query)
        
        f.close()
           
    @staticmethod
    def StockTraderData():
        start_time = time.time()
        f = open(config.logPath + config.logName_StackTraderData, 'w')
        
        dbInstance = dbConnector(sqlMap.connectInfo)
        db_stockCode = dbInstance.select(sqlMap.selectStockCode)
        db_selectParsingInfo = dbInstance.select(sqlMap.SELECTTRADERINFO_XPATH)
        db_traderInfo = dbInstance.select(sqlMap.SELECTTRADERINFO)
        
        stockLen = len(db_stockCode)
        traderLen = len(db_traderInfo)
        
        for stockIndex in range(0, stockLen):
            
            additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
            #additionalURL = "&beforeday=1"
            url = db_selectParsingInfo[0][1] + db_stockCode[stockIndex][1] + additionalURL
            xPath = db_selectParsingInfo[0][3]
            
            xPathDate = '//*[@id="contentWrap"]/h5/span/span[1]/text()'
            parseDate = htmlParser.xPathParse(url, xPathDate);
            
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
                    SC.makeQuotation(SC.todayDateFromText(parseDate[0])) + SC.comma() + \
                    SC.makeQuotation(traderName) + SC.comma() + \
                    SC.makeQuotation(buyVol) + SC.comma() + \
                    SC.makeQuotation(sellVol)
                
                VALUERESULT = VALUERESULT + SC.makeParentheses(VALUES) + SC.comma()
                #print(VALUES)
            dbInsertStatement = sqlMap.INSERTDATAWITHOUTPARENTHESES %(TABLENAME, COLUMNNAME, VALUERESULT[:-1])
            print(dbInsertStatement)
            dbInstance.insert(dbInsertStatement)
            f.write(dbInsertStatement)
            
            
        end_time = time.time()
        print("Stack the Trader Data at " + SC.todayDate() + SC.todayTime())
        print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
        f.close()
                    
    @staticmethod
    def StackFrgnData():
        start_time = time.time()
        f = open(config.logPath + config.logName_StackFrgnData, 'w')
        
        dbInstance = dbConnector(sqlMap.connectInfo)
        db_stockCode = dbInstance.select(sqlMap.selectStockCode)
        db_selectParsingInfo = dbInstance.select(sqlMap.SELECTFRGNINFO_XPATH)
        
        stockLen = len(db_stockCode)         
        TOTALVALUES = ""
        
        for stockIndex in range(0, stockLen):
             
            additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
            url = db_selectParsingInfo[0][1] + db_stockCode[stockIndex][1] + additionalURL
            xPath = db_selectParsingInfo[0][3]
            
            parseResult = htmlParser.xPathParse(url, xPath)
                
            dataLen = len(db_selectParsingInfo)    
            TABLENAME = "stock_sisae"
            COLUMNNAME = "code,date, " if dataLen is not 0 else "code,date"
            VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
                SC.makeQuotation(SC.earsePeriodMarks(parseResult[0]))
                #SC.makeQuotation("20150620")
                
                
            VALUES = VALUES + SC.comma() if dataLen is not 0 else VALUES
        
            for dataIndex in range(0, dataLen):  
               
                comma = "" if dataIndex == dataLen - 1 else SC.comma()        
                COLUMNNAME = COLUMNNAME + db_selectParsingInfo[dataIndex][0] + comma
        
                value = SC.cleanUpString(parseResult[db_selectParsingInfo[dataIndex][4]]).encode('utf8')        
                VALUES = VALUES + SC.makeQuotation(value) + comma
                #print(value)
            TOTALVALUES = TOTALVALUES + SC.makeParentheses(VALUES) + SC.comma()
            
        dbInsertStatement = sqlMap.INSERTFRGNDATA %(TOTALVALUES[:-1])
        print(dbInsertStatement)
        dbInstance.insert(dbInsertStatement)
        f.write(dbInsertStatement)
               
        end_time = time.time()
        print("Stack the Foreign and Institution Data at " + SC.todayDate() + SC.todayTime())
        print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
        f.close()
    
    @staticmethod   
    def StockShortSaleData():
        start_time = time.time()
        f = open(config.logPath + config.logName_ShortSaleData, 'w')

        dbInstance = dbConnector(sqlMap.connectInfo)
        db_stockCode = dbInstance.select(sqlMap.selectStockCode)

        TABLENAME = "stock_sisae"
        db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_px_shortSale'))
        print(db_selectParsingInfo)

        for stockIndex in range(0, len(db_stockCode)):
            url = db_selectParsingInfo[0][1] + db_stockCode[stockIndex][1] + db_selectParsingInfo[0][2]
            xPath = db_selectParsingInfo[0][3]    
            
            parseResult = htmlParser.xPathParse(url, xPath)    
                
            COLUMNNAME = "code,date,"
            VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
                SC.makeQuotation(SC.todayDate()) + SC.comma()
            
            #빈 데이터가 있을 경우(Face Value가 없음) 0으로 예외처리
            if len(parseResult) is not len(db_selectParsingInfo):
                for tempIdx in range(0, len(db_selectParsingInfo)-len(parseResult) + 10):
                    parseResult.insert(10, '0')
                    
                
            for dataIndex in range(0, len(db_selectParsingInfo)):                                                   
                comma = "" if dataIndex == len(db_selectParsingInfo) - 1 else SC.comma()            
                COLUMNNAME = COLUMNNAME + db_selectParsingInfo[dataIndex][0] + comma            
                
                if int(SC.cleanUpString(parseResult[1]))<int( SC.todayDate()) :
                    value = '0'
                else :
                    value = SC.cleanUpString(parseResult[db_selectParsingInfo[dataIndex][4]])
                                        
                VALUES = VALUES + SC.makeQuotation(value) + comma                        
            
            dbInsertStatement = sqlMap.insertStockSisaeData %(COLUMNNAME, VALUES)
            print(dbInsertStatement)
            f.write(dbInsertStatement)
            dbInstance.insert(dbInsertStatement)        
    
        end_time = time.time()
        print("Stack the Daily Short Sale Data at " + SC.todayDate() + SC.todayTime())
        print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
        
        f.write("Stack the Daily Short Sale Data at " + SC.todayDate() + SC.todayTime())
        f.write("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
        f.close()    
        
    @staticmethod   
    def StockLoanTransactionData():
        start_time = time.time()
        f = open(config.logPath + config.logName_LoanTransactionData, 'w')

        dbInstance = dbConnector(sqlMap.connectInfo)
        db_stockCode = dbInstance.select(sqlMap.selectStockCode)

        TABLENAME = "stock_sisae"
        db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_px_loanTransaction'))
        print(db_selectParsingInfo)
        for stockIndex in range(0, len(db_stockCode)):
            url = db_selectParsingInfo[0][1] + db_stockCode[stockIndex][1] + db_selectParsingInfo[0][2]
            xPath = db_selectParsingInfo[0][3]    

            parseResult = htmlParser.xPathParse(url, xPath)    
    
            COLUMNNAME = "code,date,"
            VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
                SC.makeQuotation(SC.todayDate()) + SC.comma()

            #빈 데이터가 있을 경우(Face Value가 없음) 0으로 예외처리
            if len(parseResult) is not len(db_selectParsingInfo):
                for tempIdx in range(0, len(db_selectParsingInfo)-len(parseResult) + 10):
                    parseResult.insert(10, '0')
                    
                
            for dataIndex in range(0, len(db_selectParsingInfo)):                                                   
                comma = "" if dataIndex == len(db_selectParsingInfo) - 1 else SC.comma()            
                COLUMNNAME = COLUMNNAME + db_selectParsingInfo[dataIndex][0] + comma            
                
                if int(SC.cleanUpString(parseResult[1]))<int( SC.todayDate()) :
                    value = '0'
                else :
                    value = SC.cleanUpString(parseResult[db_selectParsingInfo[dataIndex][4]])
                                        
                VALUES = VALUES + SC.makeQuotation(value) + comma                        

            dbInsertStatement = sqlMap.insertStockSisaeData %(COLUMNNAME, VALUES)
            print(dbInsertStatement)
            f.write(dbInsertStatement)
            dbInstance.insert(dbInsertStatement)        
    
        end_time = time.time()
        print("Stack the Daily Loan Transaction Data at " + SC.todayDate() + SC.todayTime())
        print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
        
        f.write("Stack the Daily Loan Transaction Data at " + SC.todayDate() + SC.todayTime())
        f.write("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
        f.close()     
    
    @staticmethod
    def StockInvestorData():
        start_time = time.time()
        f = open(config.logPath + config.logName_StockInvestorData, 'w')

        dbInstance = dbConnector(sqlMap.connectInfo)
        db_stockCode = dbInstance.select(sqlMap.selectStockCode)
        db_selectParsingInfo = dbInstance.select(sqlMap.SELECTINVESTORINFO_XPATH)
        db_investorInfo = dbInstance.select(sqlMap.SELECTINVESTORINFO)

        stockLen = len(db_stockCode)
        investorLen = len(db_investorInfo)
        
        preUrl = 'http://www.krx.co.kr/m2/m2_1/m2_1_7/JHPKOR02001_07.jsp'
        prexPath = '//*[@id="se_key"]'
        preHtml = html.parse(preUrl)
        se_key = preHtml.xpath(prexPath)[0].value
        
        increment = 11
        TABLENAME = "stock_investor"
        COLUMNNAME = "(code,date,investorCode,buyVolume,sellVolume,netVolume,buyAmount,sellAmount,netAmount)"

        for stockIndex in range(0, stockLen):

            additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
            url = db_selectParsingInfo[0][1]
            xPath = db_selectParsingInfo[0][3]    

            fr_work_dt = SC.todayDate()
            to_work_dt = SC.todayDate()
            
            stockCode = db_stockCode[stockIndex][3]
            #print(stockCode)
            isu_nm = db_stockCode[stockIndex][4] + "[" +db_stockCode[stockIndex][1] +"]" 

            parameters = '&se_key=' + se_key + \
                    '&isu_nm=' + isu_nm +\
                    '&isu_cd=' + stockCode + \
                    '&mthd=' + \
                    '&fr_work_dt=' + fr_work_dt +\
                    '&to_work_dt=' + to_work_dt + \
                    '&searchBtn=' + \
                    '&searchBtn2=%EC%A1%B0%ED%9A%8C'         
            #print(parameters)
            try:
                htm = html.parse(url + parameters)
                result = htm.xpath(xPath)
            except:
                print("ERROR")
                preHtml = html.parse(preUrl)
                se_key = preHtml.xpath(prexPath)[0].value
                time.sleep(2)
                
                parameters = '&se_key=' + se_key + \
                    '&isu_nm=' + isu_nm +\
                    '&isu_cd=' + stockCode + \
                    '&mthd=' + \
                    '&fr_work_dt=' + fr_work_dt +\
                    '&to_work_dt=' + to_work_dt + \
                    '&searchBtn=' + \
                    '&searchBtn2=%EC%A1%B0%ED%9A%8C'   
                    
                htm = html.parse(url + parameters)
                result = htm.xpath(xPath)
                   
            #print(result)
               
            invIndex = 0
            VALUERESULT = ""

            for investorIndex in range(0, len(result), increment):
                    
                buyVolumeIndex = investorIndex + db_selectParsingInfo[0][4];
                sellVolumeIndex = investorIndex + db_selectParsingInfo[1][4];
                netVolumeIndex = investorIndex + db_selectParsingInfo[2][4];
                buyAmountIndex = investorIndex + db_selectParsingInfo[3][4];
                sellAmountIndex = investorIndex + db_selectParsingInfo[4][4];
                netAmountIndex = investorIndex + db_selectParsingInfo[5][4];
                
                #print(buyVolumeIndex, sellVolumeIndex, netVolumeIndex, buyAmountIndex, sellAmountIndex, netAmountIndex)
                
                code = db_stockCode[stockIndex][0]
                date = SC.todayDate()
                investorCode = db_investorInfo[invIndex][0]        
                buyVolume = SC.cleanUpString(result[buyVolumeIndex])
                sellVolume = SC.cleanUpString(result[sellVolumeIndex])
                netVolume = SC.cleanUpString(result[netVolumeIndex])
                buyAmount = SC.cleanUpString(result[buyAmountIndex])
                sellAmount = SC.cleanUpString(result[sellAmountIndex])
                netAmount = SC.cleanUpString(result[netAmountIndex])
                        
                #print(investorCode, buyVolume, sellVolume, netVolume, buyAmount, sellAmount, netAmount)
                #print(code + " " + date +  " " + investorCode + " " + buyVolume + " " + sellVolume + " " + netVolume + " " + buyAmount + " " + sellAmount + " " + netAmount)
                        
                invIndex = invIndex + 1
                    
                VALUES = SC.makeQuotation(code) + SC.comma() + \
                    SC.makeQuotation(date) +SC.comma() + \
                    SC.makeQuotation(investorCode) +SC.comma() + \
                    SC.makeQuotation(buyVolume) +SC.comma() + \
                    SC.makeQuotation(sellVolume) +SC.comma() + \
                    SC.makeQuotation(netVolume) +SC.comma() + \
                    SC.makeQuotation(buyAmount) +SC.comma() + \
                    SC.makeQuotation(sellAmount) +SC.comma() + \
                    SC.makeQuotation(netAmount)
                
                VALUERESULT = VALUERESULT + SC.makeParentheses(VALUES) + SC.comma()
                
            dbInsertStatement = sqlMap.INSERTDATAWITHOUTPARENTHESES %(TABLENAME, COLUMNNAME, VALUERESULT[:-1])
            print(dbInsertStatement)
            dbInstance.insert(dbInsertStatement)
            f.write(dbInsertStatement)

        end_time = time.time()
        print("Stack the Daily Stock Investor Data at " + SC.todayDate() + SC.todayTime())
        print("TIME: " + repr(round(end_time - start_time, 5)) + "sec")

        f.write("Stack the Daily Stock Investor Data at " + SC.todayDate() + SC.todayTime())
        f.write("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
        f.close() 

    
