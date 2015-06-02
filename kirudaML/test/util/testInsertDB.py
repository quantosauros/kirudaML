'''
Created on 2015. 5. 27.

@author: Jay
'''
from util.sqlMap import sqlMap
from util.dbConnector import dbConnector

dbInstance = dbConnector(sqlMap.connectInfo)

#INSERT
TABLENAME = "stock_sisae"
COLUMNNAME = "code, date, currentPrice, netChange, priceChange"

VALUES = "'testCode','20150555','1' ,'1','2.12'"

dbInsertStatement = sqlMap.insertStockData %(TABLENAME, COLUMNNAME, VALUES)

print(dbInsertStatement)

dbInstance.insert(dbInsertStatement)