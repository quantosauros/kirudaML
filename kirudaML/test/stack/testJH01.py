'''
Created on 2015. 6. 15.

@author: Jay
'''
from util.sqlMap import sqlMap
from util.dbConnector import dbConnector


def ttt():
    dbInstance = dbConnector(sqlMap.connectInfo)
    
    query = "INSERT INTO STOCK_DATA (code, dt, time, current_price1, volume) \
    VALUES ('Test', '33333', '5678', '1', '2')"
    dbInstance.insert(query)