'''
Created on 2015. 5. 13.

@author: Jay
'''
from util import dbConnector
from util.sqlMap import sqlMap 

dbInstance = dbConnector.dbConnector(
            "61.96.111.174", 
            "niks12", 
            "12345", 
            "kiruda")

#INSERT
TABLENAME = "stock_data"
COLUMNNAME = "code, dt, time, current_price"
VALUES = "'testCode','20150555','1111' ,'123'"
dbInsertStatement = sqlMap.insertStockData %(TABLENAME, COLUMNNAME, VALUES)

print(dbInsertStatement)
dbInstance.insert(dbInsertStatement)

#SELECT
dbSelectStatement = sqlMap.selectStockInfo

result = dbInstance.select(dbSelectStatement)

for x in result:
    print(x)

#dbInstance.select("code", "stock_info", "")
#dbInstance.connect()


