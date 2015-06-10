# -*- coding: utf-8 -*-

import os
import sys
import getopt

from PyQt4 import QtGui


def list_tiff(_dir, prefix):
    pattern = '^%s.*(tif|tiff)$' % prefix
    match = re.compile(pattern, re.I).match
    fns = []
    for fn in os.listdir(_dir):
        fn = os.path.normcase(fn)
        if match(fn) is not None:
            fns.append(fn)
    return fns


class NewWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(NewWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        srcdirLabel  = QtGui.QLabel('Source directory')
        prefixLabel  = QtGui.QLabel('Image file prefix')
        bgndprefixLabel = QtGui.QLabel('Background image file prefix')
        darkprefixLabel = QtGui.QLabel('Dark image file prefix')

        srcdirEdit   = QtGui.QLineEdit()
        prefixEdit   = QtGui.QLineEdit()
        bgndprefixEdit  = QtGui.QLineEdit()
        darkprefixEdit  = QtGui.QLineEdit()

        srcdirBtn    = QtGui.QPushButton('Select')
        runBtn  = QtGui.QPushButton('Generate new dataset')

        prefixEdit.textChanged[str].connect(self.setImages)
        prefixEdit.textEdited[str].connect(self.setImages)

        grid1 = QtGui.QGridLayout()
        grid1.setSpacing(10)
        grid1.addWidget(srcdirLabel,  1, 0)
        grid1.addWidget(srcdirEdit,   1, 1)
        grid1.addWidget(srcdirBtn,    1, 2)
        grid1.addWidget(prefixLabel,  2, 0)
        grid1.addWidget(prefixEdit,   2, 1)
        grid1.addWidget(bgndprefixLabel, 3, 0)
        grid1.addWidget(bgndprefixEdit,  3, 1)
        grid1.addWidget(darkprefixLabel, 4, 0)
        grid1.addWidget(darkprefixEdit,  4, 1)
        group1 = QtGui.QGroupBox('Configuration')
        group1.setLayout(grid1)

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(runBtn)

        centralWidget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(centralWidget)
        vbox.addStretch(1)
        vbox.addWidget(group1)
        vbox.addLayout(hbox1)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle('New Dataset')
        self.statusBar().showMessage('Ready')
        self.show()

    def selectDirectory(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, dir=None, caption="Select directory")

    def selectFile(self):
        fn, _ = QtGui.QFileDialog.getOpenFileName(self, caption="Select file", dir=None, filter=_filter)

    def setImages(self, prefix):
        fns = list_tiff(_dir, prefix)
        self.statusBar().showMessage('%d (tiff files)' % len(self.imgs))
