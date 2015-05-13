'''
Created on 2015. 5. 13.

@author: Jay
'''
from util import dbConnector


dbInstance = dbConnector.dbConnector(
            "61.96.111.174", 
            "niks12", 
            "12345", 
            "kiruda")



#dbInstance.insert("stock_data", ("dt", "code", "time", "current_price"), ("20150513","0925" ,"123", "123"))


dbInstance.select("*", "stock_info", "")
#dbInstance.select("code", "stock_info", "")
#dbInstance.connect()


