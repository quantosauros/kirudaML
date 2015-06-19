'''
Created on 2015. 6. 19.

@author: Jay
'''
from util.dbConnector import dbConnector
from util.sqlMap import sqlMap
from lxml import html

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
print(se_key)

for stockIndex in range(0, 1):#stockLen):
    
    additionalURL = "" if db_selectParsingInfo[0][2] == None else db_selectParsingInfo[0][2]
    url = db_selectParsingInfo[0][1]
    xPath = db_selectParsingInfo[0][3]
    
    print(url)
    print(xPath)
    
    fr_work_dt ='20150612'
    to_work_dt ='20150612'
    
    print(db_stockCode[stockIndex][1])
    
    
    #===========================================================================
    # parameters = '&se_key=' + se_key + \
    #     '&isu_nm=' + isu_nm[index] +\
    #     '&isu_cd=' + stockCode[index] + \
    #     '&mthd=' + \
    #     '&fr_work_dt=' + fr_work_dt +\
    #     '&to_work_dt=' + to_work_dt + \
    #     '&searchBtn=' + \
    #     '&searchBtn2=%EC%A1%B0%ED%9A%8C' 
    #     
    #===========================================================================
    
    