from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import os
from datetime import datetime
from datadialogs import *
from listpage import *
import listpage
import datadialogs

class MainWin(QWidget):
    global activate_populatelist
    mainpage.activate_populatelist = False

    def __init__(self):
        super(MainWin, self).__init__()
        self.count = 0
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.dropdown = QComboBox(self.centralwidget)
        self.dropdown.installEventFilter(self)

    def eventFilter(self, target, event):
        if target == self.dropdown and event.type() == QtCore.QEvent.MouseButtonPress:
            print("Button press")
            self.addtobox()
        return False

    def addtobox(self):
        self.dropdown.clear()
        self.count = 1

        #load data to dropdown
        self.dropitems = LoadData(value=0, todolist=[])
        self.dropdata = self.dropitems.data_in("%%alllist.txt")

        #append data to list to be sorted
        self.sortdate = []
        for j in range(len(self.dropdata)):
            self.sortdate.append(self.dropdata[j])
        self.sortdate.sort(key=lambda date: datetime.strptime(date, "%a %b %d %Y\n"))
        print('sorted date:', self.sortdate)

        #add items to dropdown
        for i in range(len(self.sortdate)):
            self.dropdown.addItem(self.sortdate[i][:-1])

    def open_todolist(self):
        global filename
        global loaded_data
        global endloop

        #load an existing list
        mainpage.filename = self.dropdown.currentText()
        self.data = LoadData(value=0, todolist=[])
        self.data.data_out()
        mainpage.activate_populatelist = True
        print('Loaded data:', mainpage.loaded_data)

        #transfer to the next window
        self.win = QtWidgets.QWidget()
        self.listpage = ListMenu()
        self.listpage.setupUi(self.win)
        self.listpage.refreshbtn.click()
        self.win.show()

    def CreateNewList(self):
        print('Reached the new window')
        self.win = QtWidgets.QWidget()
        self.listpage = ListMenu()
        self.listpage.setupUi(self.win)
        self.win.show()

    def exit_clicked(self):
        sys.exit(1)

    def setupUi(self, MainWindow):
        #fontsize = 15
        MainWindow.resize(950, 620)
        MainWindow.setWindowTitle("To-Do List")

        #background color
        MainWindow.setStyleSheet('QMainWindow{background-color: #afafc7}')

        #click to see to do list png
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(-30, 380, 10, 181))
        self.label_2.setMaximumSize(QtCore.QSize(1000, 1000))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("Click To See To-Do Lists.png"))
        self.label_2.setScaledContents(False)
        self.label_2.lower()
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(230, 90, 851, 221))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("Click To See To-Do Lists (3).png"))
        self.label_3.lower()

        self.dropdown.setGeometry(QtCore.QRect(290, 170, 400, 51))
        self.dropdown.setEditable(True)
        self.dropdown.setCurrentText("")
        self.dropdown.setFont(QFont('consolas', 13))

        self.createButton = QtWidgets.QPushButton(self.centralwidget)
        self.createButton.setGeometry(QtCore.QRect(100, 350, 150, 150))
        self.createButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("create.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.createButton.setIcon(icon)
        self.createButton.setIconSize(QtCore.QSize(140, 160))
        self.createButton.clicked.connect(self.CreateNewList)

        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setGeometry(QtCore.QRect(420, 350, 150, 150))
        self.openButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("open.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openButton.setIcon(icon1)
        self.openButton.setIconSize(QtCore.QSize(140, 160))
        self.openButton.setObjectName("pushButton_2")
        self.openButton.clicked.connect(self.open_todolist)

        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(710, 350, 150, 150))
        self.exitButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("5844.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exitButton.setIcon(icon2)
        self.exitButton.setIconSize(QtCore.QSize(140, 160))
        self.exitButton.setObjectName("pushButton_3")
        self.exitButton.clicked.connect(self.exit_clicked)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 520, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(350, 510, 300, 61))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(750, 520, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.label.setText("Create New To-Do List")
        self.label_4.setText("Load Existing To-Do List")
        self.label_5.setText("Exit")

        MainWindow.setCentralWidget(self.centralwidget)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWin()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
