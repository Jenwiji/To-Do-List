import mainpage
from listpage import *
from abc import ABC, abstractclassmethod
from PyQt5 import QtWidgets
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

class Reply_Dialogs():
    def warning_dialog(self, dialog_type, message_show):
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage(message_show)
        error_dialog.setWindowTitle(dialog_type)
        error_dialog.exec_()

class Data(ABC):
    def __init__(self, value, todolist):
        self.value = value
        self.todolist = todolist

    @abstractclassmethod
    def data_in(self):
        pass

    @abstractclassmethod
    def data_out(self):
        pass


class LoadData(Data):
    def __init__(self, value, todolist):
        super().__init__(value, todolist)
        print('Load data')

    def data_in(self, filename):
        if os.path.exists(filename):
            fileopen = open(filename, "r")
            for data in fileopen:
                self.todolist.append(data)
        print('Before return:', self.todolist)
        return self.todolist

    def data_out(self):
        print('Filename to load: ',mainpage.filename)
        op = open(mainpage.filename+'.txt')
        mainpage.loaded_data = op.read()
        print('Loaded Data: ', mainpage.loaded_data)
        return op.read()

class SaveData(Data):
    def __init__(self, value, todolist):
        super().__init__(value, todolist)
        print('Save Data')

    def data_in(self):
        print('Data in')

        # if the list is empty, remove the file
        print('To do list: ', self.todolist)
        if self.todolist == []:
            if os.path.exists(self.value + ".txt"):
                os.remove(self.value + ".txt")
            return

        # list not empty, save the list
        print('List is saved as: ', self.value + ".txt")

        #updating old to do list
        if os.path.exists(self.value + ".txt"):
            print('File exists')
            fileopen = open(self.value[6:] + '.txt', "w+")
            print('Data out file name: ', self.value + '.txt')

            for i in range(len(self.todolist)):
                if self.todolist[i][-1] == '\U0001F31F':
                    self.todolist[i] = self.todolist[i][0:-1]

                    # save the pinned ones as percent (%)
                    self.todolist[i] = self.todolist[i] + '%'
                fileopen.write(self.todolist[i] + '\n')
                print('Item saved as: ',self.todolist[i] + '\n')
            fileopen.close()

        #a new to do list
        else:
            fileopen = open(self.value[6:] + '.txt', "w+")
            print('Data out file name: ', self.value + '.txt')

            for i in range(len(self.todolist)):
                if self.todolist[i][-1].isalpha() == False:
                    self.todolist[i] = self.todolist[i][0:-1]

                    # save the pinned ones as percent (%)
                    self.todolist[i] = self.todolist[i] + '%'
                fileopen.write(self.todolist[i] + '\n')
                print('Item saved as: ', self.todolist[i] + '\n')
            fileopen.close()

            saveall = open("%%alllist.txt", "a")
            saveall.write(self.value[6:] + '\n')  # saves all lists to open later on
            saveall.close()

    def data_out(self):
        print('Data out')
        fileopen = open(self.value + '.txt', "w+")
        print('Data out filename:', self.value + '.txt')
        print('File contents: ', fileopen.read())

        for i in range(len(self.todolist)):
            if self.todolist[i][-1].isalpha() == False:
                self.todolist[i] = self.todolist[i][0:-1]
                # save the pinned ones as percent (%)
                self.todolist[i] = self.todolist[i] + '%'
            fileopen.write(self.todolist[i] + '\n')
        fileopen.close()
