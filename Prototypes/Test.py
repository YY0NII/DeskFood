from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui, QtCore

import sys


class secondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 500, 600)
        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText("Return to menu")
        self.button1.resize(500, 100)
        self.button1.setStyleSheet("background-color: orange;font-size:18px;font-family:Times New Roman;");
        self.button1.clicked.connect(self.secondWindow)
    def secondWindow(self, checked):
        self.w = MainWindow()
        self.w.show()
        self.close()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 500, 600)
#Pop's Dining
        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText("Pop's Dining")
        self.button1.resize(500, 100)
        self.button1.setStyleSheet("background-color: orange;font-size:18px;font-family:Times New Roman;");
        self.button1.clicked.connect(self.secondWindow)
#Starbucks
        self.button2 = QtWidgets.QPushButton(self)
        self.button2.setText("Starbucks")
        self.button2.resize(500, 100)
        self.button2.setStyleSheet("background-color: green;font-size:18px;font-family:Times New Roman;");
        self.button2.clicked.connect(self.secondWindow)
        self.button2.move(0, 100)
#Freshens
        self.button3 = QtWidgets.QPushButton(self)
        self.button3.setText("Freshëns Fresh Food Studio")
        self.button3.resize(500, 100)
        self.button3.setStyleSheet("background-color: lightgreen;font-size:18px;font-family:Times New Roman;");
        
        self.button3.move(0, 200)
#Campus Center Market
        self.button4 = QtWidgets.QPushButton(self)
        self.button4.setText("Campus Center Market")
        self.button4.resize(500, 100)
        self.button4.setStyleSheet("background-color: lightblue;font-size:18px;font-family:Times New Roman;");
        
        self.button4.move(0, 300)
#Burger Studio
        self.button5 = QtWidgets.QPushButton(self)
        self.button5.setText("Burger Studio")
        self.button5.resize(500, 100)
        self.button5.setStyleSheet("background-color: lightyellow;font-size:18px;font-family:Times New Roman;");
        
        self.button5.move(0, 400)
#Boar's Head
        self.button6 = QtWidgets.QPushButton(self)
        self.button6.setText("Boar's Head")
        self.button6.resize(500, 100)
        self.button6.setStyleSheet("background-color: red;font-size:18px;font-family:Times New Roman;");
        
        self.button6.move(0, 500)

    def secondWindow(self, checked):
        self.w = secondWindow()
        self.w.show()
        self.close()
        


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()