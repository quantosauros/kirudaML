'''
Created on 2015. 5. 28.

@author: Jay
'''
from util.dbConnector import dbConnector
from util.sqlMap import sqlMap


dbInstance = dbConnector(sqlMap.connectInfo)

TABLE = 'STOCK_INFO'
COLUMNS = {'CODE', 'TICKERS', 'MARKET'}
VALUES = {'KQ000250', '000250' , 'KQ'}

for x in COLUMNS:
    print(x)
    
for y in VALUES:
    print(y)

dbInstance.insert2(TABLE, COLUMNS, VALUES) 
