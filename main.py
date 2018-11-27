# -*- coding: utf-8 -*-
# !/usr/local/bin/python3.6
# file name: main.py
from PyQt5 import QtCore, QtGui, QtWidgets
from mainWin import MainWindow
import sys

if __name__== "__main__":
    app= QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    print("exit")
    sys.exit(app.exec_())

