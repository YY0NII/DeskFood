
import sys
from PyQt5.QtWidgets import *

from PyQt5 import QtWidgets, QtGui

if __name__ == "__main__":
#this just sets up a header on the pop up looks better imo
    app = QApplication([])
    w = QWidget()
    w.setWindowTitle("DeskFood.com")
#POP's Dining
    btn1 = QPushButton("POP's Dining")
    btn1.setStyleSheet("background-color: orange;font-size:18px;font-family:Times New Roman;");
#Starbucks
    btn2 = QPushButton("Starbucks")
    btn2.setStyleSheet("background-color: green;font-size:18px;font-family:Times New Roman;");
#Freshëns Fresh Food Studio
    btn3 = QPushButton("Freshëns Fresh Food Studio")
    btn3.setStyleSheet("background-color: lightgreen;font-size:18px;font-family:Times New Roman;");
#Campus Center Market
    btn4 = QPushButton("Campus Center Market")
    btn4.setStyleSheet("background-color: lightblue;font-size:18px;font-family:Times New Roman;");
#Burger Studio
    btn5 = QPushButton("Burger Studio")
    btn5.setStyleSheet("background-color: lightyellow;font-size:18px;font-family:Times New Roman;");
#Street Food
    btn6 = QPushButton("Street Food")
    btn6.setStyleSheet("background-color: lightgrey;font-size:18px;font-family:Times New Roman;");
#TCP
    btn7 = QPushButton("TCP")
    btn7.setStyleSheet("background-color: skyblue;font-size:18px;font-family:Times New Roman;");
#Boar's Head
    btn8 = QPushButton("Boar's Head")
    btn8.setStyleSheet("background-color: red;font-size:18px;font-family:Times New Roman;");
#Book n' Beans Cafe
    btn9 = QPushButton("Book n' Beans Cafe")
    btn9.setStyleSheet("background-color: brown;font-size:18px;font-family:Times New Roman;");

    vb = QVBoxLayout(w)

    vb.addWidget(btn1)
    vb.addWidget(btn2)
    vb.addWidget(btn3)
    vb.addWidget(btn4)
    vb.addWidget(btn5)
    vb.addWidget(btn6)
    vb.addWidget(btn7)
    vb.addWidget(btn8)
    vb.addWidget(btn9)


    w.show()


sys.exit(app.exec_())



