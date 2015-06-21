#-*- coding: utf-8 -*-
'''
Created on 2015. 6. 2.

@author: Jay
'''
from lxml import html
from util.stringController import stringController as SC
from util.dbConnector import dbConnector
from util.sqlMap import sqlMap


dbInstance = dbConnector(sqlMap.connectInfo)
db_ParsingInfo = dbInstance.select(sqlMap.SELECTPARSEINGINFO %(''))
db_gicsInfo = dbInstance.select(sqlMap.SELECTGICSINFO)

work_dt = '20150619'
url = 'http://www.krx.co.kr/por_kor/corelogic/process/m1/m1_4/m1_4_8/m1_4_8_4/hpkor01004_08_04_2.xhtml?data-only=true'
xPath = '//tr/td[1]//text()'

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
    
    
    
