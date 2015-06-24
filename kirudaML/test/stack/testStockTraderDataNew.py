# -*- coding: utf8 -*-
'''
Created on 2015. 6. 19.

@author: Jay
'''
from util.dbConnector import dbConnector
from util.sqlMap import sqlMap
from lxml import html
from util.stringController import stringController as SC
import time
from lxml.html import HTMLParser
#===============================================================================
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
# print(sys.getdefaultencoding())
#===============================================================================


dbInstance = dbConnector(sqlMap.connectInfo)
db_stockCode = dbInstance.select(sqlMap.selectStockCode)
db_selectParsingInfo = dbInstance.select(sqlMap.SELECTINVESTORINFO_XPATH)
db_traderInfo = dbInstance.select(sqlMap.SELECTTRADERTESTINFO)

#print(db_selectParsingInfo)

stockLen = len(db_stockCode)
traderLen = len(db_traderInfo)

preUrl = 'http://www.krx.co.kr/m2/m2_1/m2_1_8/JHPKOR02001_08.jsp'
prexPath = '//*[@name="se_key"]'
preHtml = html.parse(preUrl)

se_key = preHtml.xpath(prexPath)[0].value
#print(se_key)

increment = 8
TABLENAME = "stock_trader_test"
COLUMNNAME = "(code,date,investorCode,buyVolume,sellVolume,netVolume,buyAmount,sellAmount,netAmount)"

for stockIndex in range(0, stockLen):
 
    #preHtml = html.parse(preUrl)
    #se_key = preHtml.xpath(prexPath)[0].value    
    #print(se_key)
    
    additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
    #url = db_selectParsingInfo[0][1]
    url = 'http://www.krx.co.kr/por_kor/corelogic/process/m2/m2_1/m2_1_8/hpkor02001_08.xhtml?data-only=true'
    
    xPath = db_selectParsingInfo[0][3]    
    #print(url)
    #print(xPath)
    
    fr_work_dt = '20150622'
    to_work_dt = '20150622'
    
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
        netVolumeIndex = parseIndex + 4
        buyAmountIndex = parseIndex + 6
        sellAmountIndex = parseIndex + 5
        netAmountIndex = parseIndex + 7
        
        #print(buyVolumeIndex, sellVolumeIndex, netVolumeIndex, buyAmountIndex, sellAmountIndex, netAmountIndex)
        
        code = db_stockCode[stockIndex][0]
        date = SC.todayDate()
                
        traderName = SC.cleanUpString(result[traderNameIndex]).encode('utf8')
        buyVolume = SC.cleanUpString(result[buyVolumeIndex]).encode('utf8')
        sellVolume = SC.cleanUpString(result[sellVolumeIndex]).encode('utf8')
        netVolume = SC.cleanUpString(result[netVolumeIndex]).encode('utf8')
        buyAmount = SC.cleanUpString(result[buyAmountIndex]).encode('utf8')
        sellAmount = SC.cleanUpString(result[sellAmountIndex]).encode('utf8')
        netAmount = SC.cleanUpString(result[netAmountIndex]).encode('utf8')

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
            SC.makeQuotation(netVolume) +SC.comma() + \
            SC.makeQuotation(buyAmount) +SC.comma() + \
            SC.makeQuotation(sellAmount) +SC.comma() + \
            SC.makeQuotation(netAmount)
        
        VALUERESULT = VALUERESULT + SC.makeParentheses(VALUES) + SC.comma()
    
    #print(VALUERESULT)    
    dbInsertStatement = sqlMap.INSERTDATAWITHOUTPARENTHESES %(TABLENAME, COLUMNNAME, VALUERESULT[:-1])
    print(dbInsertStatement)
    dbInstance.insert(dbInsertStatement)
    
    
    
    