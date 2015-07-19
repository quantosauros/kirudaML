#-*- coding: utf-8 -*-
'''
Created on 2015. 6. 2.

@author: Jay
'''
from lxml import html
from util.htmlParser import htmlParser
from util.stringController import stringController as SC
from util.dbConnector import dbConnector
from util.sqlMap import sqlMap


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

for marketIndex in range(0,3):
    
    url = db_ParsingInfo[0][1] + gubuns[marketIndex]  
    xPath = db_ParsingInfo[0][3]    
    print(url, xPath)
    
    result = htmlParser.xPathParse(url, xPath)
    totalLen = len(result)
    
    values = "("
    for index in range(0, totalLen, 7):
    
        tickerIndex = index + basetickerIndex
        nameIndex = index + basenameIndex
        krxCodeIndex = index + basekrxCodeIndex
        
        #print(tickerIndex, nameIndex, krxCodeIndex)
        
        ticker = result[tickerIndex][1:]
        name = result[nameIndex]
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
    #dbInstance.insert(query)










