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
    date = '20150619'
    
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
        time.sleep(2)
        
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
    
    
    
    