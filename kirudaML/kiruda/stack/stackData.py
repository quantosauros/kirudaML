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
import json

class stackData:

    '''
    Update Stock Lists From KRX
    '''
    @staticmethod
    def UpdateStockLists():
        
        f = open(config.logPath + config.logName_UpdateStockLists, 'w')
        
        dbInstance = dbConnector(sqlMap.connectInfo)        
        db_ParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_krx_stockList'))
        
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
            
            result = htmlParser.xPathParse(url, xPath, 'utf-8')
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
         
    '''
    Update Stock Investors for each stock From KRX
    '''            
    @staticmethod
    def StockInvestorData(date):
        start_time = time.time()
        f = open(config.logPath + config.logName_StockInvestorData, 'w')

        dbInstance = dbConnector(sqlMap.connectInfo)
        db_stockCode = dbInstance.select(sqlMap.SELECTSTOCKCODE)
        db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_krx_investor'))
        db_investorInfo = dbInstance.select(sqlMap.SELECTINVESTORINFO)
        
        #print db_selectParsingInfo
        #print db_investorInfo
        
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

            fr_work_dt = date
            to_work_dt = date
            
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
        print("Stack the Daily Stock Investor Data at " + date + SC.todayTime())
        print("TIME: " + repr(round(end_time - start_time, 5)) + "sec")

        f.write("Stack the Daily Stock Investor Data at " + date + SC.todayTime())
        f.write("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
        f.close() 

    '''
    Update Stock Prices and other information From KRX
    '''
    @staticmethod
    def StockPriceData(date):
        
        dbInstance = dbConnector(sqlMap.connectInfo)
        db_stockCode = dbInstance.select(sqlMap.SELECTSTOCKCODE)
        db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_krx_stockPrice'))
        
        #print(db_selectParsingInfo)
        
        stockLen = len(db_stockCode)
        
        preUrl = 'http://www.krx.co.kr/m2/m2_1/m2_1_4/JHPKOR02001_04.jsp'
        prexPath = '//*[@id="se_key"]'
        preHtml = html.parse(preUrl)
        se_key = preHtml.xpath(prexPath)[0].value
        gubuns = ("kospiVal", "kosdaqVal", "konexVal")
        
        TABLENAME = "stock_sisae"
        COLUMNNAME = "(code,date,currentPrice,netChange, tradingVolume,tradingSum,openPrice,highestPrice,lowestPrice,marketCap,sharesOutstanding)"
        
        for stockIndex in range(0, stockLen):
            
            code = db_stockCode[stockIndex][0]
            #date = SC.todayDate()
            #date = '20150619'
            
            additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
            url = db_selectParsingInfo[0][1]
            xPath = db_selectParsingInfo[0][3]    
        
            fr_work_dt = date
            to_work_dt = date
            
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
                try:
                    result = htm.xpath(xPath)
                except:
                    continue
             
            xpath3 = '//*[contains(@class, "down")]'
            result3 = htm.xpath(xpath3)
            sign = True if len(result3) is 0 else False
            
            #print(len(result))
            if len(result) is not 10:
                print("error")
                result.pop(1)
            
            VALUES = SC.makeQuotation(code) + SC.comma() + SC.makeQuotation(date) + SC.comma()
            for index in range(0, len(db_selectParsingInfo)):
                variable = db_selectParsingInfo[index][0]
                vIndex = db_selectParsingInfo[index][4]
                value = SC.cleanUpString(result[vIndex])
                
                if variable == 'netChange' :
                    value = value if sign is True else "-" + value
                #print(variable, vIndex, value)
               
                VALUES = VALUES + SC.makeQuotation(value) + SC.comma()
            
            #print(VALUES)
            dbInsertStatement = sqlMap.INSERTDATAWITHOUTPARENTHESES %(TABLENAME, COLUMNNAME, SC.makeParentheses(VALUES[:-1]))
            print(dbInsertStatement)
            dbInstance.insert(dbInsertStatement)
    
    '''
    Update Stock Investment Indices From KRX
    '''
    @staticmethod
    def StockInvestIndexData(date):
        dbInstance = dbConnector(sqlMap.connectInfo)
        db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_krx_investmentIndex'))
        
        #print(db_selectParsingInfo)
        
        TABLENAME = "stock_sisae"
        COLUMNNAME = "(code,date,designated, EPS,PER,BPS,PBR,dividendAmount, dividendPercent)"
        marketGubun = ('2','3')
        marketCode = ('KS','KQ')
        #date = SC.todayDate()
        
        additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
        url = db_selectParsingInfo[0][1]
        xPath = db_selectParsingInfo[0][3]    
        increment = 13
        
        for marketIndex in range(0, len(marketGubun)):
            
            #code = db_stockCode[marketIndex][0]
            #date = SC.todayDate()
            
            fr_work_dt = date
            to_work_dt = date
        
            parameters = '&market=' + \
                '&CMD=' + \
                '&cur_page=1' + \
                '&pageSize=3000' + \
                '&market_gubun=' + marketGubun[marketIndex] +\
                '&gubun=1' + \
                '&mthd=' + \
                '&fr_work_dt=' + fr_work_dt +\
                '&to_work_dt=' + to_work_dt +\
                '&searchBtn=' + \
                '&searchBtn2=%EC%A1%B0%ED%9A%8C'   
            parser1 = html.HTMLParser(encoding = 'utf8')
            
            htm = html.parse(url + parameters, parser = parser1)
            result = htm.xpath(xPath)
            #print(result)
            
            VALUERESULT = ""
            for dd in range(0, len(result), increment):
                code = marketCode[marketIndex] + result[1 + dd]
                VALUES = SC.makeQuotation(code) + SC.comma() + \
                    SC.makeQuotation(date) + SC.comma()
                  
                for index in range(0, len(db_selectParsingInfo)):
                    variable = db_selectParsingInfo[index][0]
                    vIndex = db_selectParsingInfo[index][4] + dd
                    value = SC.cleanUpString(result[vIndex]).encode('utf8')
                    #print(variable, vIndex, value)
                    if variable == 'designated':
                        value = 'Y' if value == '관리종목' else 'N' 
                    if variable == 'PER' and value == '-':
                        value = '0'
                    if variable == 'BPS' and value == '-':
                        value = '0'
                    if variable == 'PBR' and value == '-':
                        value = '0'
                    if value == '':
                        value = '0'
                          
                    VALUES = VALUES + SC.makeQuotation(value) + SC.comma()
                    
                VALUERESULT = VALUERESULT + SC.makeParentheses(VALUES[:-1]) + SC.comma()
                
            #print(VALUERESULT)
            dbInsertStatement = sqlMap.INSERTINVESTINDEXDATA %(VALUERESULT[:-1])
            print(dbInsertStatement)
            dbInstance.insert(dbInsertStatement)
    
    '''
    Update Foreign Investor's information of Stocks From KRX
    '''
    @staticmethod
    def StockForeignData(date):
        dbInstance = dbConnector(sqlMap.connectInfo)
        db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_krx_foreign'))
        
        #print(db_selectParsingInfo)
        
        TABLENAME = "stock_sisae_test"
        COLUMNNAME = "(code,date,foreignLimitStock, foreignHoldingStock)"
        marketGubun = ('kospiVal','kosdaqVal')
        marketCode = ('KS','KQ')
        indCode = ('1001', '2001')
        #date = SC.todayDate()
        additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
        url = db_selectParsingInfo[0][1]
        xPath = db_selectParsingInfo[0][3]    
        increment = 9
        
        for marketIndex in range(0, len(marketGubun)):
            
            #code = db_stockCode[marketIndex][0]
            #date = SC.todayDate()
            
            work_dt = date
           
            parameters = '&market=' + \
                '&CMD=INIT_LOAD' + \
                '&market=' + \
                '&indxIndCd=' + indCode[marketIndex] + \
                '&page_yn=Y' + \
                '&cur_page=1' + \
                '&pageSize=3000' + \
                '&market_gubun=' + marketGubun[marketIndex] +\
                '&indx_ind_cd=' + indCode[marketIndex] + \
                '&work_dt=' + work_dt + \
                '&searchBtn=' + \
                '&searchBtn2=%EC%A1%B0%ED%9A%8C'   
                
            htm = html.parse(url + parameters)
            result = htm.xpath(xPath)
            #print(result)
            
            VALUERESULT = ""
            for dd in range(0, len(result), increment):
                code = marketCode[marketIndex] + result[1 + dd]
                VALUES = SC.makeQuotation(code) + SC.comma() + \
                    SC.makeQuotation(date) + SC.comma()
                  
                for index in range(0, len(db_selectParsingInfo)):
                    variable = db_selectParsingInfo[index][0]
                    vIndex = db_selectParsingInfo[index][4] + dd
                    value = SC.cleanUpString(result[vIndex]).encode('utf8')
                    #print(code, variable, vIndex, value)
                          
                    VALUES = VALUES + SC.makeQuotation(value) + SC.comma()
                    
                VALUERESULT = VALUERESULT + SC.makeParentheses(VALUES[:-1]) + SC.comma()
                
            #print(VALUERESULT)
            dbInsertStatement = sqlMap.INSERTFOREIGNDATA %(VALUERESULT[:-1])
            print(dbInsertStatement)
            dbInstance.insert(dbInsertStatement)
    
    '''
    Update Short Sale Information of Stocks From KRX
    '''
    @staticmethod
    def StockShortSaleData(date):
        
        dbInstance = dbConnector(sqlMap.connectInfo)
        db_stockCode = dbInstance.select(sqlMap.SELECTSTOCKCODE)
        db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_krx_shortSale'))
        db_investorInfo = dbInstance.select(sqlMap.SELECTINVESTORINFO)
        
        #print(db_selectParsingInfo)
        
        stockLen = len(db_stockCode)
        investorLen = len(db_investorInfo)
        
        preUrl = 'http://www.krx.co.kr/m2/m2_1/m2_1_11/JHPKOR02001_11.jsp'
        prexPath = '//*[@id="se_key"]'
        preHtml = html.parse(preUrl)
        se_key = preHtml.xpath(prexPath)[0].value
        #print(se_key)
        
        increment = 11
        TABLENAME = "stock_sisae_test"
        COLUMNNAME = "(code,date,shortVolume, shortNotional)"
        
        for stockIndex in range(0, stockLen):
         
            #preHtml = html.parse(preUrl)
            #se_key = preHtml.xpath(prexPath)[0].value    
            #print(se_key)
            url = db_selectParsingInfo[0][1]
            xPath = db_selectParsingInfo[0][3]    
            #print(url)
            #print(xPath)
            #date = SC.todayDate()
                        
            fr_work_dt = date
            to_work_dt = date
            
            stockCode = db_stockCode[stockIndex][3]
            #print(stockCode)
            isu_nm = db_stockCode[stockIndex][4] + "[" +db_stockCode[stockIndex][1] +"]" 
            #print(stockCode)
            #print(isu_nm)
            #preHtml = html.parse(preUrl)
            #se_key = preHtml.xpath(prexPath)[0].value
            
            parameters = '?gubun=s' + \
                '&se_key=' + se_key + \
                '&jisu_sch_type=1' + \
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
                time.sleep(1)
                
                parameters = '?gubun=s' + \
                    '&se_key=' + se_key + \
                    '&jisu_sch_type=1' + \
                    '&isu_nm=' + isu_nm +\
                    '&isu_cd=' + stockCode + \
                    '&mthd=' + \
                    '&fr_work_dt=' + fr_work_dt +\
                    '&to_work_dt=' + to_work_dt + \
                    '&searchBtn=' + \
                    '&searchBtn2=%EC%A1%B0%ED%9A%8C'    
                    
                htm = html.parse(url + parameters)
                result = htm.xpath(xPath)
            
            if len(result) == 0 :
                preHtml = html.parse(preUrl)
                se_key = preHtml.xpath(prexPath)[0].value
                time.sleep(0.5)
                
                parameters = '?gubun=s' + \
                    '&se_key=' + se_key + \
                    '&jisu_sch_type=1' + \
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
            code = db_stockCode[stockIndex][0]
            if len(result) == 0:
                VALUES = SC.makeQuotation(code) + SC.comma() + SC.makeQuotation(date) + SC.comma() + "'0', '0'," 
            else:
                if SC.cleanUpString(result[0]) != date:
                    VALUES = SC.makeQuotation(code) + SC.comma() + SC.makeQuotation(date) + SC.comma() + "'0', '0',"
                else :
                    VALUES = SC.makeQuotation(code) + SC.comma() + SC.makeQuotation(date) + SC.comma()
                    for index in range(0, len(db_selectParsingInfo)):
                        variable = db_selectParsingInfo[index][0]
                        vIndex = db_selectParsingInfo[index][4]
                        value = SC.cleanUpString(result[vIndex])
                        
                        VALUES = VALUES + SC.makeQuotation(value) + SC.comma()
                
                
            dbInsertStatement = sqlMap.INSERTSHORTSALEDATA %(SC.makeParentheses(VALUES[:-1]))
            print(dbInsertStatement)
            dbInstance.insert(dbInsertStatement)
    
    '''
    Update Stock Trader Information of each stocks From KRX
    '''     
    @staticmethod
    def StockTraderData(date):
        dbInstance = dbConnector(sqlMap.connectInfo)
        db_stockCode = dbInstance.select(sqlMap.SELECTSTOCKCODE)
        db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_krx_trader'))
        db_traderInfo = dbInstance.select(sqlMap.SELECTTRADERINFO)
        
        #print(db_selectParsingInfo)
        
        stockLen = len(db_stockCode)
        traderLen = len(db_traderInfo)
        
        preUrl = 'http://www.krx.co.kr/m2/m2_1/m2_1_8/JHPKOR02001_08.jsp'
        prexPath = '//*[@name="se_key"]'
        preHtml = html.parse(preUrl)
        
        se_key = preHtml.xpath(prexPath)[0].value
        #print(se_key)
        
        increment = 8
        TABLENAME = "stock_trader"
        COLUMNNAME = "(code,date,traderCode,buyVolume,sellVolume,buyAmount,sellAmount)"
        
        for stockIndex in range(0, stockLen):
         
            #preHtml = html.parse(preUrl)
            #se_key = preHtml.xpath(prexPath)[0].value    
            #print(se_key)
            
            #additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
            url = db_selectParsingInfo[0][1]
            #url = 'http://www.krx.co.kr/por_kor/corelogic/process/m2/m2_1/m2_1_8/hpkor02001_08.xhtml?data-only=true'
            
            xPath = db_selectParsingInfo[0][3]    
            #print(url)
            #print(xPath)
            
            fr_work_dt = date
            to_work_dt = date
            
            stockCode = db_stockCode[stockIndex][3]
            #print(stockCode)
            isu_nm = db_stockCode[stockIndex][4] + "[" +db_stockCode[stockIndex][1] +"]" 
            #print(stockCode)
            #print(isu_nm)
        
            parameters = '&usr_id=' + \
                '&se_key=' + se_key + \
                '&isu_nm=' + isu_nm +\
                '&isu_cd=' + stockCode + \
                '&mthd=' + \
                '&fr_work_dt=' + fr_work_dt +\
                '&to_work_dt=' + to_work_dt + \
                '&searchBtn=' + \
                '&searchBtn2=%EC%A1%B0%ED%9A%8C'         
            #print(parameters)
            parser1 = html.HTMLParser(encoding = 'utf8')
            
            try:
                
                htm = html.parse(url + parameters, parser = parser1)
                result = htm.xpath(xPath)
            except:
                print("ERROR")
                preHtml = html.parse(preUrl)
                se_key = preHtml.xpath(prexPath)[0].value
                time.sleep(1)
                
                parameters = '&usr_id=' + \
                    '&se_key=' + se_key + \
                    '&isu_nm=' + isu_nm +\
                    '&isu_cd=' + stockCode + \
                    '&mthd=' + \
                    '&fr_work_dt=' + fr_work_dt +\
                    '&to_work_dt=' + to_work_dt + \
                    '&searchBtn=' + \
                    '&searchBtn2=%EC%A1%B0%ED%9A%8C'      
                
                try:
                    htm = html.parse(url + parameters, parser = parser1)
                    result = htm.xpath(xPath)
                except:
                    continue
                   
            #print(result)
                   
            invIndex = 0
            VALUERESULT = ""
            for parseIndex in range(0, len(result), increment):
                
                traderNameIndex = parseIndex + 1        
                buyVolumeIndex = parseIndex + 3
                sellVolumeIndex = parseIndex + 2
                buyAmountIndex = parseIndex + 6
                sellAmountIndex = parseIndex + 5
                
                #print(buyVolumeIndex, sellVolumeIndex, netVolumeIndex, buyAmountIndex, sellAmountIndex, netAmountIndex)
                
                code = db_stockCode[stockIndex][0]
                        
                traderName = SC.cleanUpString(result[traderNameIndex]).encode('utf8')
                buyVolume = SC.cleanUpString(result[buyVolumeIndex]).encode('utf8')
                sellVolume = SC.cleanUpString(result[sellVolumeIndex]).encode('utf8')
                #netVolume = SC.cleanUpString(result[netVolumeIndex]).encode('utf8')
                buyAmount = SC.cleanUpString(result[buyAmountIndex]).encode('utf8')
                sellAmount = SC.cleanUpString(result[sellAmountIndex]).encode('utf8')
                #netAmount = SC.cleanUpString(result[netAmountIndex]).encode('utf8')
        
                #print(investorCode, traderName, buyVolume, sellVolume, netVolume, buyAmount, sellAmount, netAmount)
                #print(code + " " + date +  " " + traderName + " " + buyVolume + " " + sellVolume + " " + netVolume + " " + buyAmount + " " + sellAmount + " " + netAmount)
                
                #print(traderName) 
                flag = True
                for traderIndex in range(0, traderLen):
                    #print(db_traderInfo[traderIndex][1])
                    if db_traderInfo[traderIndex][1] == traderName:
                        traderName = db_traderInfo[traderIndex][0]
                        #print(traderName)
                        flag = False
                        break
                if flag == True :
                    print(traderName)
                    
                VALUES = SC.makeQuotation(code) + SC.comma() + \
                    SC.makeQuotation(date) +SC.comma() + \
                    SC.makeQuotation(traderName) +SC.comma() + \
                    SC.makeQuotation(buyVolume) +SC.comma() + \
                    SC.makeQuotation(sellVolume) +SC.comma() + \
                    SC.makeQuotation(buyAmount) +SC.comma() + \
                    SC.makeQuotation(sellAmount)
                
                VALUERESULT = VALUERESULT + SC.makeParentheses(VALUES) + SC.comma()
            
            #print(VALUERESULT)    
            dbInsertStatement = sqlMap.INSERTDATAWITHOUTPARENTHESES %(TABLENAME, COLUMNNAME, VALUERESULT[:-1])
            print(dbInsertStatement)
            dbInstance.insert(dbInsertStatement)

    '''
    Update GICS Code for each stocks From KRX
    '''
    @staticmethod
    def UpdateGICSList(date):
        dbInstance = dbConnector(sqlMap.connectInfo)
        db_ParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_krx_gicsList'))
        db_gicsInfo = dbInstance.select(sqlMap.SELECTGICSINFO)
        
        work_dt = date
        url = db_ParsingInfo[0][1]
        xPath = db_ParsingInfo[0][3]
        
        for gicsIndex in range(0, len(db_gicsInfo)):
    
            gics_cd = db_gicsInfo[gicsIndex][0]
            #print(gics_cd)
        
            parameters = '?market_gubun=allVal' + \
                '&gics_cd=' + gics_cd + \
                '&work_dt=' + work_dt + \
                '&searchBtn=' + \
                '&searchBtn2=%EC%A1%B0%ED%9A%8C'
        
            htm = html.parse(url + parameters)
            result = htm.xpath(xPath)
        
            VALUES = ""
            for stockIndex in range(0, len(result)):
                #print(result[stockIndex])
                ticker = result[stockIndex]
                VALUES = VALUES + SC.makeQuotation(ticker) + SC.comma()
        
            #print(VALUERESULTS)
            dbInsertStatement = sqlMap.UPDATEGICSDATA \
                %(SC.makeQuotation(gics_cd), SC.makeParentheses(VALUES[:-1]))
            print(dbInsertStatement)
            dbInstance.insert(dbInsertStatement)

    '''
    Update Index Data
    '''
    @staticmethod
    def UpdateIndexData():
        dbInstance = dbConnector(sqlMap.connectInfo)
        #Korean Index
        indexCode = ('KOSPI','KOSDAQ','KPI200',)
        
        page = '1'
        for idIndex in range(0, len(indexCode)):
            url = 'http://finance.naver.com/sise/sise_index_day.nhn?code=' + \
            indexCode[idIndex] + '&page=' + page
            xPath = '*//*[contains(@class, "date")]/text() | *//*[contains(@class, "number")]/text()'
            #print(url)
            
            result = htmlParser.xPathParse(url, xPath)
            print(result)   
        
            resultLen = len(result)
        
            valueStatement = ""
        
            for index in range(0, resultLen, 6):    
                date = result[index].replace('.', '')
                value = result[index + 1].replace(',','')
                #print indexCode[idIndex], date, value
                
                tmpStatement = SC.makeQuotation(indexCode[idIndex]) + SC.comma() + \
                    SC.makeQuotation(date) + SC.comma() + \
                    SC.makeQuotation(value)
                    
                valueStatement = valueStatement + SC.makeParentheses(tmpStatement) + SC.comma()
                    
            statement = "INSERT INTO index_data (code, date, value) VALUES " + \
                valueStatement[:-1] + 'ON DUPLICATE KEY UPDATE VALUE = VALUES(VALUE)'
                
            print(statement)
            dbInstance.insert(statement)
        
        #Foreign Index
        symbols = ('DJI@DJI','DJI@DJT','NAS@IXIC','NAS@NDX','NAS@SOX',
                   'SHS@000001','SHS@000002','SHS@000003', 
                   'NII@NI225',
                   'HSI@HSI', 'HSI@HSCE', 'HSI@HSCC', 
                   'LNS@FTSE100', 'PAS@CAC40', 'XTR@DAX30')
        
        for symbolIndex in range(0, len(symbols)) :
            pageIndex = 1
            url = 'http://finance.naver.com/world/worldDayListJson.nhn?symbol=' + symbols[symbolIndex] + '&fdtc=0&page=' + repr(pageIndex)
            xPath = '*//text()'
            #xPath = '/html/body/div/table/tbody/tr/td/text()'
                
            #print(url)
            parser1 = html.HTMLParser(encoding = 'utf-8')
            htm = html.parse(url, parser = parser1)   
                         
            result = htm.xpath(xPath)
            #print result
            str = result[0][1:-2]
            splitedString = str.split('},')
            
            valueStatement = ""
            for x in splitedString :
                tmpStr = x + '}'
                #print tmpStr
                data = json.loads(tmpStr)
                #print data
                
                code = symbols[symbolIndex]
                date = data['xymd'] 
                close = repr(data['clos']) 
                open = data['open']
                high = data['high'] 
                low = data['low']
                
                #print date, close, open, high, low
                tmpStatement = SC.makeQuotation(code) + SC.comma() + \
                    SC.makeQuotation(date) + SC.comma() + \
                    SC.makeQuotation(close)
                    
                valueStatement = valueStatement + SC.makeParentheses(tmpStatement) + SC.comma()
            statement = "INSERT INTO index_data (code, date, value) VALUES " +\
                valueStatement[:-1] + 'ON DUPLICATE KEY UPDATE VALUE = VALUES(VALUE)'
                
            print statement
            dbInstance.insert(statement)
    
    '''
    Update Commodity & FX Data
    '''
    @staticmethod
    def UpdateCCData():
        dbInstance = dbConnector(sqlMap.connectInfo)
        #FX Update
        fxCode = ('FX_USDKRW', 'FX_EURKRW', 'FX_JPYKRW', 'FX_CNYKRW', 'FX_GBPKRW', 'FX_CADKRW', 'FX_AUDKRW',)
        for fxIndex in range(0, len(fxCode)):
            page = '1'
            url = 'http://info.finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=' + \
                fxCode[fxIndex] + '&page=' + page
            xPath = '/html/body/div/table/tbody/tr/td[2]/text() | /html/body/div/table/tbody/tr/td[1]/text()'    
            
            result = htmlParser.xPathParse(url, xPath)
            #print result
            resultLen = len(result)
            valueStatement = ""
            for index in range(0, resultLen, 2):
                date = result[index].replace('.', '')
                value = result[index + 1].replace(',','')
                #print fxCode[fxIndex], date, value
                
                tmpStatement = SC.makeQuotation(fxCode[fxIndex]) + SC.comma() + \
                    SC.makeQuotation(date) + SC.comma() + \
                    SC.makeQuotation(value)
                    
                valueStatement = valueStatement + SC.makeParentheses(tmpStatement) + SC.comma()
                    
            statement = "INSERT INTO cc_data (code, date, value) VALUES " +\
                valueStatement[:-1] + 'ON DUPLICATE KEY UPDATE VALUE = VALUES(VALUE)'
                
            print(statement)
            dbInstance.insert(statement)
        
        #Commodity Update
        CommodityCode = ('OIL_CL','OIL_DU','OIL_BRT','CMDT_GC')
        for commodityIndex in range(0, len(CommodityCode)):
            page = '1'    
            url = 'http://info.finance.naver.com/marketindex/worldDailyQuote.nhn?marketindexCd=' +\
                CommodityCode[commodityIndex] + '&fdtc=2' + \
                '&page=' + page
            xPath = '/html/body/div/table/tbody/tr/td[1]/text() | /html/body/div/table/tbody/tr/td[2]/text()'    
            #print(url)
            
            result = htmlParser.xPathParse(url, xPath)
            
            #print(result)
            resultLen = len(result)
            
            valueStatement = ""
            for index in range(0, resultLen, 2):
                date = SC.cleanUpString(result[index].replace('.', ''))
                value = SC.cleanUpString(result[index + 1].replace(',',''))
                #print fxCode[commodityIndex], date, value
                
                tmpStatement = SC.makeQuotation(CommodityCode[commodityIndex]) + SC.comma() + \
                    SC.makeQuotation(date) + SC.comma() + \
                    SC.makeQuotation(value)
                    
                valueStatement = valueStatement + SC.makeParentheses(tmpStatement) + SC.comma()
                    
            
            statement = "INSERT INTO cc_data (code, date, value) VALUES " +\
                valueStatement[:-1] + 'ON DUPLICATE KEY UPDATE VALUE = VALUES(VALUE)'
                
            print(statement)
            dbInstance.insert(statement)
            
            
#===============================================================================
#     #XX
#     @staticmethod
#     def StockSisaeData():
#         start_time = time.time()
#         f = open(config.logPath + config.logName_StockSisaeData, 'w')
#  
#         dbInstance = dbConnector(sqlMap.connectInfo)
#         db_stockCode = dbInstance.select(sqlMap.selectStockCode)
#         #db_selectSiteData_XPath = dbInstance.select(sqlMap.SELECTSITEDATA_XPATH %('D'))
#  
#         #parseIndex = 0
#         #stockIndex = 0
#         #dataIndex = 0
#         TABLENAME = "stock_sisae"
#         #print(db_selectSiteData_XPath)
#          
#         #for parseIndex in range(0, len(db_selectSiteData_XPath)):
#         db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_na_sisae01'))
#         #print(db_selectParsingInfo)
#  
#         for stockIndex in range(0, len(db_stockCode)):
#             #print(repr(stockIndex) +" : " + db_stockCode[stockIndex][0])
#             url = db_selectParsingInfo[0][1] + db_stockCode[stockIndex][1] + db_selectParsingInfo[0][2]
#                          
#             xPath = db_selectParsingInfo[0][3]    
#             #print(url)
#             #print(xPath)
#  
#             parseResult = htmlParser.xPathParse(url, xPath)    
#             #print(parseResult)
#      
#             COLUMNNAME = "code,date,"
#             VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
#                 SC.makeQuotation(SC.todayDate()) + SC.comma()
#  
#             #빈 데이터가 있을 경우(Face Value가 없음) 0으로 예외처리
#             if len(parseResult) is not len(db_selectParsingInfo):
#                 parseResult.insert(10, '0')
#                  
#             for dataIndex in range(0, len(db_selectParsingInfo)):                                                   
#                 comma = "" if dataIndex == len(db_selectParsingInfo) - 1 else SC.comma()            
#                 COLUMNNAME = COLUMNNAME + db_selectParsingInfo[dataIndex][0] + comma            
#                 value = SC.cleanUpString(parseResult[db_selectParsingInfo[dataIndex][4]])
#                                      
#                 #액면가가 국외통화인 경우, 통화코드 제거
#                 if db_selectParsingInfo[dataIndex][0] == 'faceValue':
#                     value = SC.cleanUpStringForFaceValue(value)
#                      
#                 VALUES = VALUES + SC.makeQuotation(value) + comma                        
#                 #print(db_selectParsingInfo[dataIndex][0] + ": " + SC.cleanUpString(value))
#          
#             #print(COLUMNNAME)
#             #print(VALUES)     
#             dbInsertStatement = sqlMap.insertStockData %(TABLENAME, COLUMNNAME, VALUES)
#             print(dbInsertStatement)
#             f.write(dbInsertStatement)
#             dbInstance.insert(dbInsertStatement)        
#      
#         end_time = time.time()
#         print("Stack the Daily Stock Data at " + SC.todayDate() + SC.todayTime())
#         print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
#          
#         f.write("Stack the Daily Stock Data at " + SC.todayDate() + SC.todayTime())
#         f.write("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
#         f.close()
# 
#     #XX
#     @staticmethod
#     def StockTraderData():
#         start_time = time.time()
#         f = open(config.logPath + config.logName_StackTraderData, 'w')
#          
#         dbInstance = dbConnector(sqlMap.connectInfo)
#         db_stockCode = dbInstance.select(sqlMap.selectStockCode)
#         db_selectParsingInfo = dbInstance.select(sqlMap.SELECTTRADERINFO_XPATH)
#         db_traderInfo = dbInstance.select(sqlMap.SELECTTRADERINFO)
#          
#         stockLen = len(db_stockCode)
#         traderLen = len(db_traderInfo)
#          
#         for stockIndex in range(0, stockLen):
#              
#             additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
#             #additionalURL = "&beforeday=1"
#             url = db_selectParsingInfo[0][1] + db_stockCode[stockIndex][1] + additionalURL
#             xPath = db_selectParsingInfo[0][3]
#              
#             xPathDate = '//*[@id="contentWrap"]/h5/span/span[1]/text()'
#             parseDate = htmlParser.xPathParse(url, xPathDate);
#              
#             parseResult = htmlParser.xPathParse(url, xPath)
#             dataLen = len(parseResult) - len(parseResult)/4
#              
#             if dataLen is 0:
#                 continue
#              
#             #print(dataLen)
#             TABLENAME = "stock_trader"
#             COLUMNNAME = "(code,date,traderCode,buyVolume,sellVolume)"
#                  
#              
#             #VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
#             #            SC.makeQuotation(SC.todayDate())
#             #VALUES = VALUES + SC.comma() if dataLen is not 0 else VALUES
#              
#             tmpData = {};   
#                  
#             for dataIndex in range(0, dataLen, 3):
#                 #comma = "" if dataIndex == dataLen - 1 else SC.comma()
#                 #COLUMNNAME = COLUMNNAME + db_selectParsingInfo[dataIndex][0] + comma
#                  
#                 traderNameIndex = db_selectParsingInfo[dataIndex][4]
#                 buyVolIndex = db_selectParsingInfo[dataIndex + 1][4]
#                 sellVolIndex = db_selectParsingInfo[dataIndex + 2][4]
#                  
#                 traderName = SC.cleanUpString(parseResult[traderNameIndex]).encode('utf8')
#                 buyVol = SC.cleanUpString(parseResult[buyVolIndex]).encode('utf8')
#                 sellVol = SC.cleanUpString(parseResult[sellVolIndex]).encode('utf8')
#                  
#                 #print(repr(dataIndex) +": "+ traderName)
#                 #print(repr(dataIndex) +": "+ buyVol)
#                 #print(repr(dataIndex) +": "+ sellVol)
#                  
#                 flag = True
#                 for traderIndex in range(0, traderLen):
#                     if db_traderInfo[traderIndex][1] == traderName:
#                         traderName = db_traderInfo[traderIndex][0]
#                         #print(traderName)
#                         flag = False
#                         break
#                 if flag == True :
#                     print(traderName)
#                 #print(repr(dataIndex) + ": " + traderName)    
#                 #VALUES = VALUES + SC.makeQuotation(traderName) + comma
#                 tmpData[traderName] = (buyVol, sellVol)
#                 #print(tmpData)
#                  
#             VALUERESULT = ""
#      
#             for data in tmpData:
#                  
#                 traderName = data
#                 buyVol = tmpData[data][0]
#                 sellVol = tmpData[data][1]
#                  
#                 VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
#                     SC.makeQuotation(SC.todayDateFromText(parseDate[0])) + SC.comma() + \
#                     SC.makeQuotation(traderName) + SC.comma() + \
#                     SC.makeQuotation(buyVol) + SC.comma() + \
#                     SC.makeQuotation(sellVol)
#                  
#                 VALUERESULT = VALUERESULT + SC.makeParentheses(VALUES) + SC.comma()
#                 #print(VALUES)
#             dbInsertStatement = sqlMap.INSERTDATAWITHOUTPARENTHESES %(TABLENAME, COLUMNNAME, VALUERESULT[:-1])
#             print(dbInsertStatement)
#             dbInstance.insert(dbInsertStatement)
#             f.write(dbInsertStatement)
#              
#              
#         end_time = time.time()
#         print("Stack the Trader Data at " + SC.todayDate() + SC.todayTime())
#         print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
#         f.close()
#      
#      
#     #XX     
#     @staticmethod
#     def StackFrgnData():
#         start_time = time.time()
#         f = open(config.logPath + config.logName_StackFrgnData, 'w')
#           
#         dbInstance = dbConnector(sqlMap.connectInfo)
#         db_stockCode = dbInstance.select(sqlMap.selectStockCode)
#         db_selectParsingInfo = dbInstance.select(sqlMap.SELECTFRGNINFO_XPATH)
#           
#         stockLen = len(db_stockCode)         
#         TOTALVALUES = ""
#           
#         for stockIndex in range(0, stockLen):
#                
#             additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
#             url = db_selectParsingInfo[0][1] + db_stockCode[stockIndex][1] + additionalURL
#             xPath = db_selectParsingInfo[0][3]
#               
#             parseResult = htmlParser.xPathParse(url, xPath)
#                   
#             dataLen = len(db_selectParsingInfo)    
#             TABLENAME = "stock_sisae"
#             COLUMNNAME = "code,date, " if dataLen is not 0 else "code,date"
#             VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
#                 SC.makeQuotation(SC.earsePeriodMarks(parseResult[0]))
#                 #SC.makeQuotation("20150620")
#                   
#                   
#             VALUES = VALUES + SC.comma() if dataLen is not 0 else VALUES
#           
#             for dataIndex in range(0, dataLen):  
#                  
#                 comma = "" if dataIndex == dataLen - 1 else SC.comma()        
#                 COLUMNNAME = COLUMNNAME + db_selectParsingInfo[dataIndex][0] + comma
#           
#                 value = SC.cleanUpString(parseResult[db_selectParsingInfo[dataIndex][4]]).encode('utf8')        
#                 VALUES = VALUES + SC.makeQuotation(value) + comma
#                 #print(value)
#             TOTALVALUES = TOTALVALUES + SC.makeParentheses(VALUES) + SC.comma()
#               
#         dbInsertStatement = sqlMap.INSERTFRGNDATA %(TOTALVALUES[:-1])
#         print(dbInsertStatement)
#         dbInstance.insert(dbInsertStatement)
#         f.write(dbInsertStatement)
#                  
#         end_time = time.time()
#         print("Stack the Foreign and Institution Data at " + SC.todayDate() + SC.todayTime())
#         print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
#         f.close()
#      
#     #XX
#     @staticmethod   
#     def StockShortSaleData():
#         start_time = time.time()
#         f = open(config.logPath + config.logName_ShortSaleData, 'w')
#   
#         dbInstance = dbConnector(sqlMap.connectInfo)
#         db_stockCode = dbInstance.select(sqlMap.selectStockCode)
#   
#         TABLENAME = "stock_sisae"
#         db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_px_shortSale'))
#         print(db_selectParsingInfo)
#   
#         for stockIndex in range(0, len(db_stockCode)):
#             url = db_selectParsingInfo[0][1] + db_stockCode[stockIndex][1] + db_selectParsingInfo[0][2]
#             xPath = db_selectParsingInfo[0][3]    
#               
#             parseResult = htmlParser.xPathParse(url, xPath)    
#                   
#             COLUMNNAME = "code,date,"
#             VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
#                 SC.makeQuotation(SC.todayDate()) + SC.comma()
#               
#             #빈 데이터가 있을 경우(Face Value가 없음) 0으로 예외처리
#             if len(parseResult) is not len(db_selectParsingInfo):
#                 for tempIdx in range(0, len(db_selectParsingInfo)-len(parseResult) + 10):
#                     parseResult.insert(10, '0')
#                       
#                   
#             for dataIndex in range(0, len(db_selectParsingInfo)):                                                   
#                 comma = "" if dataIndex == len(db_selectParsingInfo) - 1 else SC.comma()            
#                 COLUMNNAME = COLUMNNAME + db_selectParsingInfo[dataIndex][0] + comma            
#                   
#                 if int(SC.cleanUpString(parseResult[1]))<int( SC.todayDate()) :
#                     value = '0'
#                 else :
#                     value = SC.cleanUpString(parseResult[db_selectParsingInfo[dataIndex][4]])
#                                           
#                 VALUES = VALUES + SC.makeQuotation(value) + comma                        
#               
#             dbInsertStatement = sqlMap.insertStockSisaeData %(COLUMNNAME, VALUES)
#             print(dbInsertStatement)
#             f.write(dbInsertStatement)
#             dbInstance.insert(dbInsertStatement)        
#       
#         end_time = time.time()
#         print("Stack the Daily Short Sale Data at " + SC.todayDate() + SC.todayTime())
#         print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
#           
#         f.write("Stack the Daily Short Sale Data at " + SC.todayDate() + SC.todayTime())
#         f.write("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
#         f.close()    
#      
#     #XX  
#     @staticmethod   
#     def StockLoanTransactionData():
#         start_time = time.time()
#         f = open(config.logPath + config.logName_LoanTransactionData, 'w')
#  
#         dbInstance = dbConnector(sqlMap.connectInfo)
#         db_stockCode = dbInstance.select(sqlMap.selectStockCode)
#  
#         TABLENAME = "stock_sisae"
#         db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_px_loanTransaction'))
#         print(db_selectParsingInfo)
#         for stockIndex in range(0, len(db_stockCode)):
#             url = db_selectParsingInfo[0][1] + db_stockCode[stockIndex][1] + db_selectParsingInfo[0][2]
#             xPath = db_selectParsingInfo[0][3]    
#  
#             parseResult = htmlParser.xPathParse(url, xPath)    
#      
#             COLUMNNAME = "code,date,"
#             VALUES = SC.makeQuotation(db_stockCode[stockIndex][0]) + SC.comma() + \
#                 SC.makeQuotation(SC.todayDate()) + SC.comma()
#  
#             #빈 데이터가 있을 경우(Face Value가 없음) 0으로 예외처리
#             if len(parseResult) is not len(db_selectParsingInfo):
#                 for tempIdx in range(0, len(db_selectParsingInfo)-len(parseResult) + 10):
#                     parseResult.insert(10, '0')
#                      
#                  
#             for dataIndex in range(0, len(db_selectParsingInfo)):                                                   
#                 comma = "" if dataIndex == len(db_selectParsingInfo) - 1 else SC.comma()            
#                 COLUMNNAME = COLUMNNAME + db_selectParsingInfo[dataIndex][0] + comma            
#                  
#                 if int(SC.cleanUpString(parseResult[1]))<int( SC.todayDate()) :
#                     value = '0'
#                 else :
#                     value = SC.cleanUpString(parseResult[db_selectParsingInfo[dataIndex][4]])
#                                          
#                 VALUES = VALUES + SC.makeQuotation(value) + comma                        
#  
#             dbInsertStatement = sqlMap.insertStockSisaeData %(COLUMNNAME, VALUES)
#             print(dbInsertStatement)
#             f.write(dbInsertStatement)
#             dbInstance.insert(dbInsertStatement)        
#      
#         end_time = time.time()
#         print("Stack the Daily Loan Transaction Data at " + SC.todayDate() + SC.todayTime())
#         print ("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
#          
#         f.write("Stack the Daily Loan Transaction Data at " + SC.todayDate() + SC.todayTime())
#         f.write("TIME: " + repr(round(end_time - start_time, 5)) + "sec")
#         f.close()     
#===============================================================================
     
        
