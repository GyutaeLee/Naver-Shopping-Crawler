import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets
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
        
        self.firstQVBoxLayout = []

        self.firstQVBoxLayout.append(QVBoxLayout())
        self.firstQVBoxLayout.append(QVBoxLayout())

        self.firstLayout.addLayout(self.firstQVBoxLayout[0])

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
        
    def CreateNewButtonForCategory(self, buttonText, buttonMethod, index):
        return self.CreateNewButton(buttonText, lambda: buttonMethod(index))

    ##
    ##
    def InitializeWindow(self, bigCategoryTextList, categoryTextList, crawlingMethod):
        self.crawlingMethod = crawlingMethod

        # #
        self.qFormLabel = self.CreateNewLabel("카테고리 선택")
        self.qFormLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.qFormLabel.setMinimumWidth(300)
        self.firstQVBoxLayout[0].addWidget(self.qFormLabel)

      #  self.DrawLine(10,10,20,20, Qt.black, 10, Qt.SolidLine)

        self.bigCategoryButtonList  = ['' for first in range(len(bigCategoryTextList))]
        self.categoryCheckBoxList = ['' for first in range(len(categoryTextList))]

        self.qFrame = [QFrame() for i in range(len(categoryTextList))]
        self.secondQGridLayout = [QGridLayout() for i in range(len(categoryTextList))]

        for index in range(0, len(categoryTextList)):
            self.categoryCheckBoxList[index] = ['' for first in range(len(categoryTextList[index]))]

        for index in range(0, len(bigCategoryTextList)):
            self.bigCategoryButtonList[index] = self.CreateNewButtonForCategory(bigCategoryTextList[index], self.SelectCategory, index)
            self.firstQVBoxLayout[0].addWidget(self.bigCategoryButtonList[index])

        #
        self.categoryButtonList = [QPushButton for i in range(0, len(categoryTextList))]

        for index in range(0, len(categoryTextList)): #?? 하나가 더 많다 이상하게
            row = 0
            column = 0

            self.qFrame[index].setLayout(self.secondQGridLayout[index])
            self.qFrame[index].hide()
            self.firstLayout.addWidget(self.qFrame[index])

            self.categoryButtonList[index] = self.CreateNewButtonForCategory("전체 체크", self.CheckAllSmallCategory, index)
            self.secondQGridLayout[index].addWidget(self.categoryButtonList[index], row, column)
            
            for jindex in range(0, len(categoryTextList[index])):

                row += 1
                if row >= 20:
                    column += 1
                    row = 0

                self.categoryCheckBoxList[index][jindex] = self.CreateNewCheckBox(categoryTextList[index][jindex], None)
                self.secondQGridLayout[index].addWidget(self.categoryCheckBoxList[index][jindex], row, column)
                

        self.pageCount     = self.LabelWithLineEdit(self, "PAGE COUNT")
        self.excelFileName = self.LabelWithLineEdit(self, "FILE NAME")
        self.startButton   = self.CreateNewButton("시작", self.StartCrawling)

        ##
        self.firstLayout.addLayout(self.firstQVBoxLayout[1])

        for index in range(0, len(self.labelList)):
            self.firstQVBoxLayout[1].addWidget(self.labelList[index], self.lineButtonList[index])
        
        self.firstQVBoxLayout[1].addWidget(self.pageCount)
        self.firstQVBoxLayout[1].addWidget(self.excelFileName)
        self.firstQVBoxLayout[1].addWidget(self.startButton)

    ##
    def OpenPopupMessageBox(self, title, content): 
        buttonReply = QMessageBox.information(
            self, title, content, 
            QMessageBox.Yes)


    ##
    def StartCrawling(self):
        if self.pageCount.lineEdit.text() == "" or self.excelFileName.lineEdit.text() == "":
            self.OpenPopupMessageBox("오류", "내용을 입력하고 크롤링을 시작해주세요.")
            return
        
        print("----------------------------------------------------")
        print("크롤링 시작")
        print("----------------------------------------------------")

        # create bool List
        boolList = [False for first in range(len(self.categoryCheckBoxList))]
        for index in range(0, len(self.categoryCheckBoxList)):
            boolList[index] = [False for second in range(len(self.categoryCheckBoxList[index]))]
            for jindex in range(0, len(self.categoryCheckBoxList[index])):
                boolList[index][jindex] = self.categoryCheckBoxList[index][jindex].isChecked()

        self.crawlingMethod(int(self.pageCount.lineEdit.text()), self.excelFileName.lineEdit.text(), boolList)
        
    def CheckAllSmallCategory(self, index):
        if self.categoryCheckBoxList[index][0].isChecked() == True:
            boolean = False
        else:
            boolean = True

        for i in range(0, len(self.categoryCheckBoxList[index])):
            self.categoryCheckBoxList[index][i].setChecked(boolean)

    def SelectCategory(self, index):
        for i in range(0, len(self.bigCategoryButtonList)):
            if i != index:
                self.qFrame[i].hide()
            else:
                self.qFrame[i].show()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )