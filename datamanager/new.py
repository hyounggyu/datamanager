# -*- coding: utf-8 -*-

import os
import sys
import re
import getopt

from PyQt4 import QtGui


MSGBASE = '''{} images, {} bgnds, {} darks
tgt: {}'''

def list_tiff(_dir, prefix):
    if _dir == None or prefix == '':
        return []

    pattern = '^{}.*(tif|tiff)$'.format(prefix)
    match = re.compile(pattern, re.I).match
    fns = []
    for fn in os.listdir(_dir):
        fn = os.path.normcase(fn)
        if match(fn) is not None:
            fns.append(fn)

    return fns


class NewWindow(QtGui.QMainWindow):

    srcdir = None
    tgtfname = None

    def __init__(self, parent=None):
        super(NewWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.srcdirLabel  = QtGui.QLabel('Source directory')
        self.srcdirLabel.setFixedWidth(200)
        self.srcdirBtn    = QtGui.QPushButton('Select')
        self.srcdirBtn.clicked.connect(self.selectSourceDirectory)

        self.prefixLabel  = QtGui.QLabel('Image file prefix')
        self.prefixEdit   = QtGui.QLineEdit()
        self.prefixEdit.textChanged[str].connect(self.countImages)
        self.prefixEdit.textEdited[str].connect(self.countImages)

        self.bgndprefixLabel = QtGui.QLabel('Background image file prefix')
        self.bgndprefixEdit  = QtGui.QLineEdit()
        self.bgndprefixEdit.textChanged[str].connect(self.countImages)
        self.bgndprefixEdit.textEdited[str].connect(self.countImages)

        self.darkprefixLabel = QtGui.QLabel('Dark image file prefix')
        self.darkprefixEdit  = QtGui.QLineEdit()
        self.darkprefixEdit.textChanged[str].connect(self.countImages)
        self.darkprefixEdit.textEdited[str].connect(self.countImages)

        grid1 = QtGui.QGridLayout()
        grid1.setSpacing(10)
        grid1.addWidget(self.srcdirLabel,  0, 0)
        grid1.addWidget(self.srcdirBtn,    0, 1)
        grid1.addWidget(self.prefixLabel,  1, 0)
        grid1.addWidget(self.prefixEdit,   1, 1)
        grid1.addWidget(self.bgndprefixLabel, 2, 0)
        grid1.addWidget(self.bgndprefixEdit,  2, 1)
        grid1.addWidget(self.darkprefixLabel, 3, 0)
        grid1.addWidget(self.darkprefixEdit,  3, 1)
        group1 = QtGui.QGroupBox('Source Configuration')
        group1.setLayout(grid1)

        self.tgtfileLabel  = QtGui.QLabel('Export file name')
        self.tgtfileLabel.setFixedWidth(200)
        self.tgtfileBtn    = QtGui.QPushButton('Select')
        self.tgtfileBtn.clicked.connect(self.selectTargetFilename)

        grid2 = QtGui.QGridLayout()
        grid2.setSpacing(10)
        grid2.addWidget(self.tgtfileLabel, 0, 0)
        grid2.addWidget(self.tgtfileBtn,   0, 1)
        group2 = QtGui.QGroupBox('Target Configuration')
        group2.setLayout(grid2)

        self.dateLabel = QtGui.QLabel('Experiment Date')
        self.dateEdit = QtGui.QLabel('TODO:')

        grid3 = QtGui.QGridLayout()
        grid3.setSpacing(10)
        grid3.addWidget(self.dateLabel, 0, 0)
        grid3.addWidget(self.dateEdit,  0, 1)
        group3 = QtGui.QGroupBox('Experiment Configuration')
        group3.setLayout(grid3)

        runBtn  = QtGui.QPushButton('Generate new dataset')
        runBtn.clicked.connect(self.run)

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(runBtn)

        centralWidget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(centralWidget)
        vbox.addStretch(1)
        vbox.addWidget(group1)
        vbox.addWidget(group2)
        vbox.addWidget(group3)
        vbox.addLayout(hbox1)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle('New Dataset')
        self.statusBar().showMessage('Ready')
        self.show()

    def selectSourceDirectory(self):
        _dir = QtGui.QFileDialog.getExistingDirectory(self, caption="Select source directory")
        if _dir != '':
            self.srcdir = _dir
            self.statusBar().showMessage('{} directory selected.'.format(os.path.basename(self.srcdir)))

    def selectTargetFilename(self):
        fn = QtGui.QFileDialog.getSaveFileName(self, caption="Select target file")
        if fn != '':
            self.tgtfname = fn
            self.statusBar().showMessage('{} file selected.'.format(os.path.basename(self.tgtfname)))

    def countImages(self, prefix):
        fns = list_tiff(self.srcdir, prefix)
        self.statusBar().showMessage('{} image files selected.'.format(len(fns)))

    def run(self):
        image_prefix = self.prefixEdit.text()
        bgnd_prefix = self.bgndprefixEdit.text()
        dark_prefix = self.darkprefixEdit.text()

        images = list_tiff(self.srcdir, image_prefix)
        bgnds = list_tiff(self.srcdir, bgnd_prefix)
        darks = list_tiff(self.srcdir, dark_prefix)

        # 소스 디렉토리, 타켓 파일 점검하기
        msg = MSGBASE.format(len(images), len(bgnds), len(darks), os.path.basename(self.tgtfname))

        msgbox = QtGui.QMessageBox(self)
        msgbox.setText('ㅇㅋ?')
        msgbox.setInformativeText(msg)
        msgbox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        msgbox.setDefaultButton(QtGui.QMessageBox.Cancel);
        ret = msgbox.exec_()

        # image 파일이 하나도 없을 때 처리
        # ret 값에 따라 처리
        # HDF5 그룹과 데이터셋 이름 정하기
