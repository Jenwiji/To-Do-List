from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import os
import datadialogs as ddl2
import mainpage
from datetime import datetime
from abc import ABC, abstractclassmethod

class ListMenu(object):
    global appended_tolist
    appended_tolist = []

    def __init__(self):
        self.star = '\U0001F31F'

    def setupUi(self, win):
        self.win = win
        self.win.resize(950, 620)
        self.win.setWindowTitle("To-Do List")
        fontsize = 15
        self.todolist = []

        #big list
        self.list = QListWidget(win)
        self.list.setGeometry(QtCore.QRect(20, 60, 451, 551))
        self.list.setFont(QFont('consolas', 15))
        self.list.setStyleSheet("QListWidget{background : #afafc7;" "}" "QListView::item:selected"
            "{""border : 2px solid black;""background : #5F7DAF;""}")

        #calendar widget
        self.cal = QtWidgets.QCalendarWidget(win)
        self.cal.setGeometry(QtCore.QRect(500, 50, 421, 251))
        self.cal.clicked.connect(self.selectedDate)
        self.cal.setStyleSheet("background-color : #E2C3C8;")
        self.value = self.cal.selectedDate().toString()

        #date label on top of list
        self.l1 = QtWidgets.QLabel(win)
        self.l1.setGeometry(QtCore.QRect(40, 20, 411, 31))
        self.l1.setFont(QFont('consolas', fontsize))
        self.l1.setText("Date :{}".format(self.value))

        self.addbtn = QtWidgets.QPushButton(win)
        self.addbtn.setGeometry(QtCore.QRect(520, 330, 181, 71))
        self.addbtn.setFont(QFont('consolas', fontsize))
        self.addbtn.clicked.connect(self.add_clicked)
        self.addbtn.setStyleSheet('background-color : #F7DFD3')
        self.addbtn.setText("Add")

        self.editbtn = QtWidgets.QPushButton(win)
        self.editbtn.setGeometry(QtCore.QRect(520, 400, 181, 71))
        self.editbtn.setFont(QFont('consolas', fontsize))
        self.editbtn.clicked.connect(self.edit_clicked)
        self.editbtn.setStyleSheet('background-color : #F7DFD3')
        self.editbtn.setText("Edit")

        self.removebtn = QtWidgets.QPushButton(win)
        self.removebtn.setGeometry(QtCore.QRect(520, 470, 181, 71))
        self.removebtn.setFont(QFont('consolas', fontsize))
        self.removebtn.clicked.connect(self.remove_clicked)
        self.removebtn.setStyleSheet('background-color : #F7DFD3')
        self.removebtn.setText("Remove")

        self.savebtn = QtWidgets.QPushButton(win)
        self.savebtn.setGeometry(QtCore.QRect(730, 470, 181, 71))
        self.savebtn.setFont(QFont('consolas', fontsize))
        self.savebtn.clicked.connect(self.save_clicked)
        self.savebtn.setStyleSheet('background-color : #F7DFD3')
        self.savebtn.setText("Save")

        self.starbtn = QtWidgets.QPushButton(win)
        self.starbtn.setGeometry(QtCore.QRect(730, 330, 181, 71))
        self.starbtn.setFont(QFont('consolas', fontsize))
        self.starbtn.clicked.connect(self.set_starred)
        self.starbtn.setStyleSheet('background-color : #F7DFD3')
        self.starbtn.setText("PIN")

        self.unstarbtn = QtWidgets.QPushButton(win)
        self.unstarbtn.setGeometry(QtCore.QRect(730, 400, 181, 71))
        self.unstarbtn.setFont(QFont('consolas', fontsize))
        self.unstarbtn.clicked.connect(self.unpin)
        self.unstarbtn.setStyleSheet('background-color : #F7DFD3')
        self.unstarbtn.setText("UNPIN")

        self.clearbtn = QtWidgets.QPushButton(win)
        self.clearbtn.setGeometry(QtCore.QRect(520, 540, 181, 71))
        self.clearbtn.setFont(QFont('consolas', fontsize))
        self.clearbtn.clicked.connect(self.clear_clicked)
        self.clearbtn.setStyleSheet('background-color : #F7DFD3')
        self.clearbtn.setText("Clear")

        self.backbtn = QtWidgets.QPushButton(win)
        self.backbtn.setGeometry(QtCore.QRect(730, 540, 181, 71))
        self.backbtn.setFont(QFont('consolas', fontsize))
        self.backbtn.setText("Back")
        self.backbtn.setStyleSheet('background-color : #F7DFD3')
        self.backbtn.clicked.connect(self.back_clicked)

        self.checkbtn = QtWidgets.QPushButton(win)
        self.checkbtn.setVisible(False)
        self.checkbtn.clicked.connect(self.ischecked)

        self.refreshbtn = QtWidgets.QPushButton(win)

        self.refreshbtn.setVisible(False)
        self.refreshbtn.clicked.connect(self.refresh)

        self.label_2 = QtWidgets.QLabel(win)
        self.label_2.setGeometry(QtCore.QRect(560, 270, 341, 41))
        self.label_2.setObjectName("label_2")

        self.list.setAlternatingRowColors(True)
        self.list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.list.setDropIndicatorShown(True)

    def refresh(self):
        self.l1.setText('Date: {}'.format(mainpage.filename))
        alltasks = mainpage.loaded_data
        self.alltasks_list = alltasks.split("\n")

        temp = []
        for j in range(len(self.alltasks_list)):
            if self.alltasks_list[j] != '':
                temp.append(self.alltasks_list[j])
            count = j
        print('temp', temp)
        temptemp = temp
        for i in range(count):
            print('Task: ', self.alltasks_list[i])

            if self.alltasks_list[i][-1] == '%':
                temp = self.alltasks_list[i][:-1]
                item = QtWidgets.QListWidgetItem(temp + self.star)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Unchecked)
                if '^' in self.alltasks_list[i]:
                    temp = self.alltasks_list[i][:-1]
                    temp = temp.replace('^', '')
                    item = QtWidgets.QListWidgetItem(temp + self.star)
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                    item.setCheckState(QtCore.Qt.Checked)
            else:
                temp = self.alltasks_list[i]
                item = QtWidgets.QListWidgetItem(temp)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Unchecked)
                if '^' in self.alltasks_list[i]:
                    temp = self.alltasks_list[i]
                    temp = temp.replace('^', '')
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                    item = QtWidgets.QListWidgetItem(temp)
                    item.setCheckState(QtCore.Qt.Checked)

            if self.alltasks_list[i] not in appended_tolist and self.alltasks_list[i] != '':
                self.list.addItem(item)
            appended_tolist.append(i)
        self.todolist = temptemp
        print('To do list: ', self.todolist)
        self.cal.setDisabled(True)

    def selectedDate(self):
        if mainpage.activate_populatelist == 1:
            value = self.cal.selectedDate().toString()
            self.l1.setText('Date: {}'.format(value))
            self.l1.setFont(QFont('consolas', 15))
        else:
            value = self.cal.selectedDate().toString()
            self.l1.setText('Date: {}'.format(value))
            self.l1.setFont(QFont('consolas', 15))

    def add_clicked(self):
        row = self.list.currentRow()
        checktask = []

        self.task_to_add, okPressed = QtWidgets.QInputDialog.getText(None, "Add Task",
        "Task: ", QtWidgets.QLineEdit.Normal, "")
        print(self.task_to_add)
        checktask.append(self.task_to_add)
        print(checktask)
        if checktask == ['']:
            print('an error')
            warning = ddl2.Reply_Dialogs()
            warning.warning_dialog('ERROR', 'Invalid Input')

        elif all(string.isalpha() or string.isspace() or string.isdigit() for string in self.task_to_add):
            self.task_to_add = self.task_to_add.title()
            self.todolist.append(self.task_to_add)
            item = QtWidgets.QListWidgetItem(self.task_to_add)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.list.addItem(item)

        elif okPressed == False:
            return

    def edit_clicked(self):
        row = self.list.currentRow()
        item = self.list.item(row)
        if item is not None:
            title = "Edit Task"
            task_to_edit, okPressed = QtWidgets.QInputDialog.getText(None, title,
                    "Task: ", QtWidgets.QLineEdit.Normal, "")
            if task_to_edit is not None and all(string.isalpha() or string.isspace() or string.isdigit() for string in task_to_edit):
                item.setText(task_to_edit)

    def set_starred(self):
        row = self.list.currentRow()
        item = self.list.item(row)
        starred = item.text()
        print('Item to set pin:', starred)
        print('To do list', self.todolist)

        if item is not None and starred[-1] != '%' and starred[-1] != '\U0001F31F':
            print('condition satisfied')
            # star emoji
            self.star = '\U0001F31F'

            #find the index
            try:
                starindex = self.todolist.index(starred)
            except:
                starindex = self.todolist.index('^' + starred)

            self.todolist[starindex] = self.todolist[starindex] + self.star
            item = QtWidgets.QListWidgetItem(starred + self.star)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if '^' in self.todolist[starindex]:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

            # set the check item to first row
            firstitem = item
            self.list.insertItem(0, firstitem)
            item = self.list.takeItem(row + 1)
            del item

        else:
            reply = QMessageBox.information(self.win, '', 'Already Pinned')

    def unpin(self):
        row = self.list.currentRow()
        item = self.list.item(row)
        current_text = item.text()
        if current_text[-1].isalpha() == True:
            return
        else:
            item.setText(current_text[:-1])

    def remove_clicked(self):
        row = self.list.currentRow()
        item = self.list.item(row)
        if item is None:
            return
        reply = QMessageBox.question(self.win, 'Remove', "Are you sure you want to Remove?", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            item = self.list.takeItem(row)
            del item

    def ischecked(self):
        print('Is checked Function:')
        count = self.list.count()
        print('Number of items in list:', count)

        for i in range(count):
            #if the task is checked, append the ^ in front
            if self.list.item(i).checkState() == QtCore.Qt.Checked:
                if '^' not in self.todolist[i]:
                    self.todolist[i] = '^' + self.todolist[i]
                print('checked')
            #if the task is not unchecked (previously checked) replace the ^ with blank
            elif self.list.item(i).checkState() == QtCore.Qt.Unchecked:
                if '^' in self.todolist[i]:
                    self.todolist[i] = self.todolist[i].replace('^', '')
                print('unchekced')

    def save_clicked(self):
        self.checkbtn.click()

        # get selected date
        self.value = self.l1.text()
        self.count = self.list.count()

        # if the task is checked, append ^ in front
        self.todolist = []
        for i in range(self.count):
            self.todolist.append(self.list.item(i).text())
            if self.list.item(i).checkState() == QtCore.Qt.Checked:
                self.todolist[i] = '^' + self.todolist[i]
                print('Appended:', self.todolist[i])
        print('thisistemplist', self.todolist)

        self.sortdate = []
        self.sortdate.append(self.value)
        print('To do list before saving:', self.todolist)

        #replace the star with percent to save
        for x in self.todolist:
            if self.star in x:
                x.replace(self.star, '%')
        print('before saved:', self.todolist)

        # call save function
        tosave = ddl2.SaveData(self.value, self.todolist)
        tosave.data_in()
        tosave.data_out()

        saved = ddl2.Reply_Dialogs()
        saved.warning_dialog('SAVED', 'Your List Has Been Saved!')

    def clear_clicked(self):
        reply = QMessageBox.question(self.win, "Clear List", "Clear entire list?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.list.clear()

    def back_clicked(self):
        self.win.hide()
