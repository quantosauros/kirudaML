# -*- coding: utf8 -*-
'''
Created on 2015. 6. 19.

@author: Jay
'''
from util.dbConnector import dbConnector
from util.sqlMap import sqlMap
from lxml import html
from util.htmlParser import htmlParser
from util.stringController import stringController as SC
import time

dbInstance = dbConnector(sqlMap.connectInfo)
db_stockCode = dbInstance.select(sqlMap.selectStockCode)
db_selectParsingInfo = dbInstance.select(sqlMap.SELECTINVESTORINFO_XPATH)
db_investorInfo = dbInstance.select(sqlMap.SELECTINVESTORINFO)

#print(db_selectParsingInfo)

stockLen = len(db_stockCode)
investorLen = len(db_investorInfo)

preUrl = 'http://www.krx.co.kr/m2/m2_1/m2_1_7/JHPKOR02001_07.jsp'
prexPath = '//*[@id="se_key"]'
preHtml = html.parse(preUrl)
se_key = preHtml.xpath(prexPath)[0].value
print(se_key)

increment = 11
TABLENAME = "stock_investor"
COLUMNNAME = "(code,date,investorCode,buyVolume,sellVolume,netVolume,buyAmount,sellAmount,netAmount)"

for stockIndex in range(0, stockLen):
 
    #preHtml = html.parse(preUrl)
    #se_key = preHtml.xpath(prexPath)[0].value    
    #print(se_key)
    
    additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
    url = db_selectParsingInfo[0][1]
    xPath = db_selectParsingInfo[0][3]    
    #print(url)
    #print(xPath)
    
    fr_work_dt = SC.todayDate()
    to_work_dt = SC.todayDate()
    
    stockCode = db_stockCode[stockIndex][3]
    print(stockCode)
    isu_nm = db_stockCode[stockIndex][4] + "[" +db_stockCode[stockIndex][1] +"]" 
    #print(stockCode)
    #print(isu_nm)
    
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
                
        print(investorCode, buyVolume, sellVolume, netVolume, buyAmount, sellAmount, netAmount)
        print(code + " " + date +  " " + investorCode + " " + buyVolume + " " + sellVolume + " " + netVolume + " " + buyAmount + " " + sellAmount + " " + netAmount)
                
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
    #dbInstance.insert(dbInsertStatement)
    
    
    
    