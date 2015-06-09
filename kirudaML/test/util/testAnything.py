'''
Created on 2015. 6. 5.

@author: Jay
'''
from util.dbConnector import dbConnector
from util.sqlMap import sqlMap
from util.stringController import stringController


dbInstance = dbConnector(sqlMap.connectInfo)

TABLE = 'STOCK_INFO'
COLUMNS = {'CODE', 'TICKERS', 'MARKET'}
VALUES = {'KQ000250', '000250' , 'KQ'}

val = "'KQ000250', '000250', 'KQ'"

query = sqlMap.insertStockList %(val)

print(query)

dbInstance.insert(query)

 
