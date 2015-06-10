# -*- coding: utf-8 -*-

import os
import sys
import re
import getopt

from PyQt4 import QtGui


def list_tiff(_dir, prefix):
    if _dir == None:
        return []

    pattern = '^%s.*(tif|tiff)$' % prefix
    match = re.compile(pattern, re.I).match
    fns = []
    for fn in os.listdir(_dir):
        fn = os.path.normcase(fn)
        if match(fn) is not None:
            fns.append(fn)
    return fns


class NewWindow(QtGui.QMainWindow):

    _dir = None
    images = None
    bgndimages = None
    darkimages = None

    def __init__(self, parent=None):
        super(NewWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        srcdirLabel  = QtGui.QLabel('Source directory')
        srcdirLabel.setFixedWidth(200)
        srcdirBtn    = QtGui.QPushButton('Select')
        srcdirBtn.clicked.connect(self.selectDirectory)

        prefixLabel  = QtGui.QLabel('Image file prefix')
        prefixEdit   = QtGui.QLineEdit()
        prefixEdit.textChanged[str].connect(self.setImages)
        prefixEdit.textEdited[str].connect(self.setImages)

        bgndprefixLabel = QtGui.QLabel('Background image file prefix')
        bgndprefixEdit  = QtGui.QLineEdit()
        bgndprefixEdit.textChanged[str].connect(self.setBgndImages)
        bgndprefixEdit.textEdited[str].connect(self.setBgndImages)

        darkprefixLabel = QtGui.QLabel('Dark image file prefix')
        darkprefixEdit  = QtGui.QLineEdit()
        darkprefixEdit.textChanged[str].connect(self.setDarkImages)
        darkprefixEdit.textEdited[str].connect(self.setDarkImages)

        grid1 = QtGui.QGridLayout()
        grid1.setSpacing(10)
        grid1.addWidget(srcdirLabel,  0, 0)
        grid1.addWidget(srcdirBtn,    0, 1)
        grid1.addWidget(prefixLabel,  1, 0)
        grid1.addWidget(prefixEdit,   1, 1)
        grid1.addWidget(bgndprefixLabel, 2, 0)
        grid1.addWidget(bgndprefixEdit,  2, 1)
        grid1.addWidget(darkprefixLabel, 3, 0)
        grid1.addWidget(darkprefixEdit,  3, 1)
        group1 = QtGui.QGroupBox('Source Configuration')
        group1.setLayout(grid1)

        destdirLabel  = QtGui.QLabel('Destination directory')
        destdirLabel.setFixedWidth(200)
        destdirBtn    = QtGui.QPushButton('Select')
        destdirBtn.clicked.connect(self.selectDirectory)

        h5fileLabel  = QtGui.QLabel('Dataset Filename')
        h5fileEdit   = QtGui.QLineEdit()
        h5fileEdit.textChanged[str].connect(self.setImages)
        h5fileEdit.textEdited[str].connect(self.setImages)

        grid2 = QtGui.QGridLayout()
        grid2.setSpacing(10)
        grid2.addWidget(destdirLabel, 0, 0)
        grid2.addWidget(destdirBtn,   0, 1)
        grid2.addWidget(h5fileLabel,  1, 0)
        grid2.addWidget(h5fileEdit,   1, 1)
        group2 = QtGui.QGroupBox('Destination Configuration')
        group2.setLayout(grid2)

        runBtn  = QtGui.QPushButton('Generate new dataset')
        runBtn.clicked.connect(self.run)

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(runBtn)

        centralWidget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(centralWidget)
        vbox.addStretch(1)
        vbox.addWidget(group1)
        vbox.addWidget(group2)
        vbox.addLayout(hbox1)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle('New Dataset')
        self.statusBar().showMessage('Ready')
        self.show()

    def selectDirectory(self):
        self._dir = QtGui.QFileDialog.getExistingDirectory(self, caption="Select directory")
        if self._dir != '':
            self.statusBar().showMessage('"{}" directory selected.'.format(os.path.basename(self._dir)))

    def setImages(self, prefix):
        fns = list_tiff(self._dir, prefix)
        self.statusBar().showMessage('{} image files selected.'.format(len(fns)))

    def setBgndImages(self, prefix):
        fns = list_tiff(self._dir, prefix)
        self.statusBar().showMessage('{} background files selected.'.format(len(fns)))

    def setDarkImages(self, prefix):
        fns = list_tiff(self._dir, prefix)
        self.statusBar().showMessage('{} dark files selected.'.format(len(fns)))

    def run(self):
        msg = 'test'
        msgbox = QtGui.QMessageBox(self)
        msgbox.setText(msg)
        msgbox.setInformativeText(msg)
        msgbox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        msgbox.setDefaultButton(QtGui.QMessageBox.Cancel);
        ret = msgbox.exec_()
