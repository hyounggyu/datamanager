# -*- coding: utf-8 -*-

import os
import getopt
import re
import sys
import time

from PyQt4 import QtCore, QtGui
import h5py

from .tifffile import imread


class Worker(QtCore.QObject):

    finished = QtCore.pyqtSignal()
    relay = QtCore.pyqtSignal(int)
    isFinished = False

    def __init__(self, output, images, bgnds=[], darks=[], 
        groupname='original',
        images_dsetname='images',
        bgnds_dsetname='bgnds',
        darks_dsetname='darks',
        dtype='i2',
        parent=None):

        super(Worker, self).__init__(parent)

        self.images = images
        self.bgnds = bgnds
        self.darks = darks
        self.images_dsetname = images_dsetname
        self.bgnds_dsetname = bgnds_dsetname
        self.darks_dsetname = darks_dsetname
        self.dtype = dtype

    def process(self):
        ny, nx = imread(self.images[0]).shape # All images are same shape

        self.fd = h5py.File(output, 'w')
        self.grp = self.fd.create_group(groupname)

        sub_run(bgnds_dsetname, self.bgnds, ny, nx)
        sub_run(darks_dsetname, self.darks, ny, nx)

        self.images_dset = self.grp.create_dataset(self.images_dsetname, (len(self.images), ny, nx), dtype=dtype)
        for i in range(len(self.images)):
            if self.isFinished == True:
                break
            images_dset[i,:,:] = imread(self.images[i])[:,:]
            self.relay.emit(i)
            QtGui.QApplication.processEvents()

        self.fd.close()
        self.finished.emit()

    def sub_run(self, dsetname, flist, ny, nx):
        if len(flist) > 0:
            dset = self.grp.create_dataset(dsetname, (len(flist), ny, nx), dtype=self.dtype)
            for i in range(len(flist)):
                dset[i,:,:] = imread(flist[i])[:,:]

    def stop(self):
        self.isFinished = True


class NewWindow(QtGui.QMainWindow):

    _dir = None
    output = None

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

        self.runBtn = QtGui.QPushButton('Generate new dataset')
        self.runBtn.clicked.connect(self.run)

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.runBtn)

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
            self.output = fn
            self.statusBar().showMessage('{} file selected.'.format(os.path.basename(self.output)))

    def _list(self, prefix):
        if self._dir == None or self._dir == '':
            return []
        pattern = '^{}.*(tif|tiff)$'.format(prefix)
        match = re.compile(pattern, re.I).match
        fns = []
        for fn in os.listdir(self._dir):
            fn = os.path.normcase(fn)
            if match(fn) is not None:
                fns.append(fn)
        return sorted(fns)

    def countImages(self, prefix):
        fns = self._list(prefix)
        self.statusBar().showMessage('{} image files selected.'.format(len(fns)))

    def run(self):
        image_prefix = self.prefixEdit.text()
        images = self._list(image_prefix)

        if image_prefix == '':
            self.warning('Image prefix is empty.')

        if len(images) == 0:
            self.warning('Can not find images.')
            return

        bgnd_prefix = self.bgndprefixEdit.text()
        dark_prefix = self.darkprefixEdit.text()
        bgnds = self._list(bgnd_prefix) if bgnd_prefix != '' else []
        darks = self._list(dark_prefix) if dark_prefix != '' else []

        if self.output == None:
            self.warning('Target file is None.')
            return

        ret = self.confirm(self.output, images, bgnds, darks)

        if ret == QtGui.QMessageBox.Ok:
            self.thread = QtCore.QThread()
            self.worker = Worker(self.output, images, bgnds, darks)
            self.progress = QtGui.QProgressDialog("Progress","Cancel",0,len(images))
            self.thread.started.connect(self.worker.process)
            self.worker.moveToThread(self.thread)
            self.worker.relay.connect(self.progress.setValue)
            self.worker.finished.connect(self.thread.quit)
            self.progress.canceled.connect(self.worker.stop)
            self.thread.start()
            self.progress.exec_()
            if self.progress.wasCanceled():
                pass

    def confirm(self, output, images, bgnds, darks):
        msg = '''Number of images: {}
Number of Background images: {}
Number of Dark images: {}
HDF5 filename: {}'''.format(len(images), len(bgnds), len(darks), os.path.basename(output))

        msgbox = QtGui.QMessageBox(self)
        msgbox.setText('Really?')
        msgbox.setInformativeText(msg)
        msgbox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        msgbox.setDefaultButton(QtGui.QMessageBox.Cancel);
        return msgbox.exec_()

    def warning(self, msg):
        msgbox = QtGui.QMessageBox(self)
        msgbox.setText(msg)
        msgbox.exec_()
