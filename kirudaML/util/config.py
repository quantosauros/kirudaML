'''
Created on 2015. 6. 9.

@author: Jay
'''
from util.stringController import stringController as SC

class config:
    
    logPath = "D:\\KirudaML_LOG\\"
    logName_StockSisaeData = "log_StockSisaeData_" + SC.todayDate() + ".txt"
    logName_UpdateStockLists = "log_UpdateStockLists_" + SC.todayDate() + ".txt"