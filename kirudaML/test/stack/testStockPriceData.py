'''
Created on 2015. 6. 20.

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
db_selectParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %('xpath_krx_stockPrice'))

#print(db_selectParsingInfo)

stockLen = len(db_stockCode)

preUrl = 'http://www.krx.co.kr/m2/m2_1/m2_1_4/JHPKOR02001_04.jsp'
prexPath = '//*[@id="se_key"]'
preHtml = html.parse(preUrl)
se_key = preHtml.xpath(prexPath)[0].value
gubuns = ("kospiVal", "kosdaqVal", "konexVal")

TABLENAME = "stock_sisae_test"
COLUMNNAME = "(code,date,currentPrice, netChange,tradingVolume,tradingSum,openPrice,highestPrice,lowestPrice,marketCap,sharesOutstanding)"

for stockIndex in range(0, stockLen):
    
    code = db_stockCode[stockIndex][0]
    #date = SC.todayDate()
    date = '20150108'
    
    additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
    url = db_selectParsingInfo[0][1]
    xPath = '//tr/td//text()'#db_selectParsingInfo[0][3]    

    fr_work_dt = date
    to_work_dt = date
    
    stockCode = db_stockCode[stockIndex][3]
    print(stockCode)
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
        result = htm.xpath(xPath)
     
    xpath3 = '//*[contains(@class, "down")]'
    result3 = htm.xpath(xpath3)
    sign = True if len(result3) is 0 else False
    
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
    
    
