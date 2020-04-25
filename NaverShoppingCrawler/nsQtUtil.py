import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize    

class MainWindow(QMainWindow):
    
    class LabelWithLineEdit(QWidget):
        def __init__(self, mainHandle, text):
            super(QWidget, self).__init__()

            self.mainWindowHandle = mainHandle

            self.lineEdit = self.mainWindowHandle.CreateNewLine()
            self.label    = self.mainWindowHandle.CreateNewLabel(text)
            
            self.widgetLayout = QHBoxLayout(self)

            self.widgetLayout.addWidget(self.lineEdit)
            self.widgetLayout.addWidget(self.label)
        
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout(self.mainWidget)

        self.firstLayout = QHBoxLayout()
        self.secondLayout = QHBoxLayout()

        self.mainLayout.addLayout(self.firstLayout)
        self.mainLayout.addLayout(self.secondLayout)

        self.setCentralWidget(self.mainWidget)
        
        self.textBoxFormLayout = QFormLayout()        
        self.firstLayout.addLayout(self.textBoxFormLayout)                     
        
    def CreateNewLabel(self, nameLabelText):       
        newLabel = QLabel(self)
        newLabel.setText(nameLabelText)
        return newLabel

    def CreateNewLine(self):
        newLine = QLineEdit(self)
        return newLine

    def CreateButton(self, buttonText, buttonMethod):
        newButton = QPushButton(buttonText, self)
        newButton.clicked.connect(buttonMethod)
        return newButton

    def InitInputDataLabel(self):      
                
        self.startDateLabel                          = self.CreateNewLabel("시작 날짜(YEAR / MONTH / DAY)")
        self.lastDateLabel                           = self.CreateNewLabel("종료 날짜(YEAR / MONTH / DAY)")
        self.stockItemPageNumberLabel                 = self.CreateNewLabel("주식 종목 페이지 개수")
        self.standardOfAscendingLabel                = self.CreateNewLabel("기준 등락률")
        self.standardOfTransactionAmountLabel        = self.CreateNewLabel("기준 거래 대금")
        self.kospiFileNameLabel                      = self.CreateNewLabel("코스피 엑셀 이름")
        self.kospiSheetNameLabel                     = self.CreateNewLabel("코스피 시트 이름")
        self.kosdacFileNameLabel                     = self.CreateNewLabel("코스닥 엑셀 이름")
        self.kosdacSheetNameLabel                    = self.CreateNewLabel("코스닥 시트 이름")

        self.startDate = self.LabelWithLineEdit(self, "20200101 (숫자만 입력하세요 : yyyymmdd)")
        self.lastDate  = self.LabelWithLineEdit(self, "20200105 (숫자만 입력하세요 : yyyymmdd)")
        self.stockItemPageNumber = self.LabelWithLineEdit(self, "주식 정보 페이지 개수 (-1은 모든 주식 종목 검색)")
        self.standardOfAscending  = self.LabelWithLineEdit(self, "1 (숫자만 입력하세요 [1~100])")
        self.standardOfTransactionAmount  = self.LabelWithLineEdit(self, "1 (숫자만 입력하세요)")
        self.kospiFileName  = self.LabelWithLineEdit(self, "코스피 엑셀 이름")
        self.kospiSheetName  = self.LabelWithLineEdit(self, "코스피 시트 이름")
        self.kosdacFileName  = self.LabelWithLineEdit(self, "코스닥 엑셀 이름")
        self.kosdacSheetName  = self.LabelWithLineEdit(self, "코스닥 시트 이름")

        self.textBoxFormLayout.addRow(self.startDateLabel, self.startDate)
        self.textBoxFormLayout.addRow(self.lastDateLabel, self.lastDate)
        self.textBoxFormLayout.addRow(self.stockItemPageNumberLabel, self.stockItemPageNumber)
        self.textBoxFormLayout.addRow(self.standardOfAscendingLabel, self.standardOfAscending)
        self.textBoxFormLayout.addRow(self.standardOfTransactionAmountLabel, self.standardOfTransactionAmount)
        self.textBoxFormLayout.addRow(self.kospiFileNameLabel, self.kospiFileName)
        self.textBoxFormLayout.addRow(self.kospiSheetNameLabel, self.kospiSheetName)
        self.textBoxFormLayout.addRow(self.kosdacFileNameLabel, self.kosdacFileName)
        self.textBoxFormLayout.addRow(self.kosdacSheetNameLabel, self.kosdacSheetName)        
        
        self.debugLabel = []

        self.debugLabel.append(self.CreateNewLabel("조건을 입력 후 버튼을 눌러주세요"))
        self.debugLabel.append(self.CreateNewLabel("조건을 입력 후 버튼을 눌러주세요"))
        
        self.secondLayout.addWidget(self.debugLabel[0])
        self.secondLayout.addWidget(self.debugLabel[1])

    def RefrestInputDataLabel(self):
        self.startDate.label.setText(self.startDate.lineEdit.text())
        self.lastDate.label.setText(self.lastDate.lineEdit.text())
        self.stockItemPageNumber.label.setText(self.stockItemPageNumber.lineEdit.text())
        self.standardOfAscending.label.setText(self.standardOfAscending.lineEdit.text())
        self.standardOfTransactionAmount.label.setText(self.standardOfTransactionAmount.lineEdit.text())
        self.kospiFileName.label.setText(self.kospiFileName.lineEdit.text())
        self.kospiSheetName.label.setText(self.kospiSheetName.lineEdit.text())
        self.kosdacFileName.label.setText(self.kosdacFileName.lineEdit.text())
        self.kosdacSheetName.label.setText(self.kosdacSheetName.lineEdit.text())                                            

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
