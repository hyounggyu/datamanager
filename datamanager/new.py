# -*- coding: utf-8 -*-

import os
import sys
import getopt

from PyQt4 import QtGui


class NewWindow(QtGui.QMainWindow):

    def __init__(self, dataset=None, parent=None):
        super(MainWindow, self).__init__(parent)
        self.dataset = dataset
        self.initUI()

    def initUI(self):
        self.srcdirLabel  = QtGui.QLabel('Source directory')
        self.prefixLabel  = QtGui.QLabel('Image file prefix')
        self.bgndimgLabel = QtGui.QLabel('Background image file')
        self.darkimgLabel = QtGui.QLabel('Dark image file')
        self.sftdirLabel  = QtGui.QLabel('Shifted image directory')
        self.posfnLabel   = QtGui.QLabel('Position data file')

        self.srcdirEdit   = QtGui.QLineEdit()
        self.prefixEdit   = QtGui.QLineEdit()
        self.bgndimgEdit  = QtGui.QLineEdit()
        self.darkimgEdit  = QtGui.QLineEdit()
        self.sftdirEdit   = QtGui.QLineEdit()
        self.posfnEdit    = QtGui.QLineEdit()

        self.srcdirBtn    = QtGui.QPushButton('Select')
        self.bgndimgBtn   = QtGui.QPushButton('Select')
        self.darkimgBtn   = QtGui.QPushButton('Select')
        self.sftdirBtn    = QtGui.QPushButton('Select')
        self.posfnBtn     = QtGui.QPushButton('Select')
        self.plotshiftBtn = QtGui.QPushButton('Plot')
        self.runshiftBtn  = QtGui.QPushButton('Run')

        grid1 = QtGui.QGridLayout()
        grid1.setSpacing(10)
        grid1.addWidget(self.srcdirLabel,  1, 0)
        grid1.addWidget(self.srcdirEdit,   1, 1)
        grid1.addWidget(self.srcdirBtn,    1, 2)
        grid1.addWidget(self.prefixLabel,  2, 0)
        grid1.addWidget(self.prefixEdit,   2, 1)
        grid1.addWidget(self.bgndimgLabel, 3, 0)
        grid1.addWidget(self.bgndimgEdit,  3, 1)
        grid1.addWidget(self.bgndimgBtn,   3, 2)
        grid1.addWidget(self.darkimgLabel, 4, 0)
        grid1.addWidget(self.darkimgEdit,  4, 1)
        grid1.addWidget(self.darkimgBtn,   4, 2)
        group1 = QtGui.QGroupBox('Base Configuration')
        group1.setLayout(grid1)

        grid2 = QtGui.QGridLayout()
        grid2.setSpacing(10)
        grid2.addWidget(self.sftdirLabel,  1, 0)
        grid2.addWidget(self.sftdirEdit,   1, 1)
        grid2.addWidget(self.sftdirBtn,    1, 2)
        grid2.addWidget(self.posfnLabel,   2, 0)
        grid2.addWidget(self.posfnEdit,    2, 1)
        grid2.addWidget(self.posfnBtn,     2, 2)
        group2 = QtGui.QGroupBox('Shift Configuration')
        group2.setLayout(grid2)

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.plotshiftBtn)
        hbox1.addWidget(self.runshiftBtn)

        centralWidget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(centralWidget)
        vbox.addStretch(1)
        vbox.addWidget(group1)
        vbox.addWidget(group2)
        vbox.addLayout(hbox1)
        self.setCentralWidget(centralWidget)

        self.statusBar().showMessage('Ready')

    def open(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, caption='Select file')

    def selectDirectory(self, widget):
        directory = QtGui.QFileDialog.getExistingDirectory(self, dir=None, caption="Select directory")
        #widget.setText(directory)

    def selectFile(self, widget, _filter):
        fn, _ = QtGui.QFileDialog.getOpenFileName(self, caption="Select file", dir=None, filter=_filter)
        #widget.setText(fn)
