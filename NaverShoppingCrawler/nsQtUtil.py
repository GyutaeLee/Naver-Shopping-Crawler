import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPainterPath
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt

class MainWindow(QMainWindow):
    
    ## CLASS
    class LabelWithLineEdit(QWidget):
        def __init__(self, mainHandle, text):
            super(QWidget, self).__init__()

            self.mainWindowHandle = mainHandle

            self.label    = self.mainWindowHandle.CreateNewLabel(text)
            self.lineEdit = self.mainWindowHandle.CreateNewLine()
            
            self.widgetLayout = QHBoxLayout(self)

            self.widgetLayout.addWidget(self.label)
            self.widgetLayout.addWidget(self.lineEdit)

    class LineEditWithButton(QWidget):
        def __init__(self, mainHandle, text, buttonMethod):
            super(QWidget, self).__init__()
            
            self.mainWindowHandle = mainHandle

            self.lineEdit = self.mainWindowHandle.CreateNewLine()
            self.button   = mainHandle.CreateNewButton(text, buttonMethod)

            self.widgetLayout = QHBoxLayout(self)
            
            self.lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.lineEdit.setMinimumWidth(50)

            self.widgetLayout.addWidget(self.lineEdit)
            self.widgetLayout.addWidget(self.button)            

    class DrawLine(QWidget):
        def __init__(self, x1, y1, x2, y2, color, scale, style):
            super().__init__()
            
            self.qPainter = QPainter()
            self.qPainter.begin(self)

            self.qPen = QPen(color, scale, style)
            self.qPainter.setPen(self.qPen)
            self.qPainter.drawLine(x1,y1,x2,y2)

            self.qPainter.end()            


    def __init__(self):
        QMainWindow.__init__(self)
        
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout(self.mainWidget)

        self.firstLayout = QHBoxLayout()

        self.mainLayout.addLayout(self.firstLayout)

        self.setCentralWidget(self.mainWidget)
        
        self.firstQFormLayout = []

        for index in range(0,2):
            self.firstQFormLayout.append(QFormLayout())
            self.firstLayout.addLayout(self.firstQFormLayout[index])

        self.labelList = []
        self.lineButtonList  = []
           
        self.pageCount = 0
        self.excelFileName = ''
    
    ##
    ##
    def CreateNewLabel(self, nameLabelText):       
        newLabel = QLabel(self)
        newLabel.setText(nameLabelText)
        return newLabel

    def CreateNewLine(self):
        newLine = QLineEdit(self)
        return newLine

    def CreateNewButton(self, buttonText, buttonMethod):
        newButton = QPushButton(buttonText, self)
        newButton.clicked.connect(buttonMethod)
        return newButton

    def CreateNewCheckBox(self, checkBoxText, checkBoxMethod):
        newCheckBox = QCheckBox(checkBoxText, self)
        newCheckBox.stateChanged.connect(lambda: checkBoxMethod)
        return newCheckBox

    def CreateLabelAndLineButtonList(self, labelList, lineButtonList, labelName, buttonName, buttonMethod):
        labelList.append(self.CreateNewLabel(labelName))
        lineButtonList.append(self.LineEditWithButton(self, buttonName, lambda: buttonMethod))
        
    ##
    ##
    def InitializeWindow(self, textList, crawlingMethod):
        self.crawlingMethod = crawlingMethod

        # #
        self.qFormLabel = self.CreateNewLabel("카테고리 선택")
        self.qFormLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.qFormLabel.setMinimumWidth(150)
        self.firstQFormLayout[0].addRow(self.qFormLabel)

      #  self.DrawLine(10,10,20,20, Qt.black, 10, Qt.SolidLine)

        self.checkBoxList  = ['' for first in range(len(textList))]
        self.checkBoxState = [False for first in range(len(textList))]

        for index in range(0, len(textList)):
            self.checkBoxList[index] = (self.CreateNewCheckBox(textList[index], None))
            self.firstQFormLayout[0].addRow(self.checkBoxList[index])

        self.pageCount     = self.LabelWithLineEdit(self, "PAGE COUNT")
        self.excelFileName = self.LabelWithLineEdit(self, "FILE NAME")
        self.startButton   = self.CreateNewButton("시작", self.StartCrawling)

        for index in range(0, len(self.labelList)):
            self.firstQFormLayout[1].addRow(self.labelList[index], self.lineButtonList[index])
        
        self.firstQFormLayout[1].addRow(self.pageCount)
        self.firstQFormLayout[1].addRow(self.excelFileName)
        self.firstQFormLayout[1].addRow(self.startButton)

    ##
    def StartCrawling(self):
        print("크롤링 시작\n")

        # create bool List
        boolList = [False for b in range(len(self.checkBoxList))]
        for index in range(0, len(self.checkBoxList)):
            boolList[index] = self.checkBoxList[index].isChecked()

        self.crawlingMethod(int(self.pageCount.lineEdit.text()), self.excelFileName.lineEdit.text(), boolList)

    def ChangeBoolState(self, index):
        self.checkBoxState[index] = self.checkBoxList[index].isChecked()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )