#-*- coding: utf-8 -*-
'''
Created on 2015. 6. 15.

@author: Jay
'''
import sys
from PyQt4 import QtGui, QtCore, uic
from datetime import datetime
from kiruda.stack.stackData import stackData


var = True
class Main(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()
        self.ui.show()
    def initUI(self):
        self.ui = uic.loadUi("testUi.ui")
        self.ui.pushButton_1.clicked.connect(self.pushButton1_clicked)
        self.ui.pushButton_2.clicked.connect(self.pushButton2_clicked)

#-------- Slots ------------------------------------------
    def Time(self):
        global var
        currentTime = datetime.now()
        timeStr = currentTime.strftime("%H%M%S")
        #오후4시 주식목록 업데이트
        if timeStr == "161100" and var == True:
            var = False
            stackData.UpdateStockLists()
            self.ui.label_2.setText("Updated Stock Lists.")
            var = True
        #오후4시5분 주식시세 업데이트
        elif timeStr == "161300" and var == True:
            var = False
            stackData.StockSisaeData()
            self.ui.label_2.setText("Updated Stock Sisae.")
            var = True
        #오후 10시30분 거래원 거래정보 업데이트
        elif timeStr == "223000" and var == True:
            var = False
            stackData.StockTraderData()
            self.ui.label_2.setText("Update Stock Traders.")
            var = True
        #오후 10시 45분 투자자별 거래실적 업데이
        elif timeStr == "224500" and var == True:
            var = False
            stackData.StockInvestorData()
            self.ui.label_2.setText("Update Stock Investor Data.")
            var = True
        #오후 11시 00분 공매도 거래 정보 업데이트
        elif timeStr == "230000" and var == True:
            var = False
            stackData.StockShortSaleData()
            self.ui.label_2.setText("Update ShortSale Data.")
            var = True
        #오후 11시 30분  대차거래 정보 업데이트
        elif timeStr == "233000" and var == True:
            var = False
            stackData.StockLoanTransactionData()
            self.ui.label_2.setText("Update Loan Transaction Data.")
            var = True
        #elif timeStr == "001500" and var == True:
        #    self.ui.label_2.setText("AAAAAAAAAAAAAAAA")
        else :
            timeStr = currentTime.strftime("%Y-%m-%d %H:%M:%S")
            self.ui.label_1.setText(timeStr)
        
    def pushButton1_clicked(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(10)
        
    def pushButton2_clicked(self):
        self.timer.stop()
        
def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()