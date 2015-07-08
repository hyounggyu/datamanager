import os
import getopt
import re
import sys
import time
from pathlib import Path

from PyQt4 import QtCore, QtGui

from xni.io import dataset


class Worker(QtCore.QObject):

    finished = QtCore.pyqtSignal()
    relay = QtCore.pyqtSignal(int)
    isFinished = False

    def __init__(self, output, images, bgnds=[], darks=[], parent=None):
        super(Worker, self).__init__(parent)
        self.output = output
        self.images = images
        self.bgnds = bgnds
        self.darks = darks

    def process(self):
        map_obj = dataset.create(self.output, self.images, self.bgnds, self.darks)
        for i, _ in map_obj:
            if self.isFinished == True:
                break
            self.relay.emit(i)
            QtGui.QApplication.processEvents()
        self.finished.emit()

    def stop(self):
        self.isFinished = True


class CreateWindow(QtGui.QMainWindow):

    _dir = None
    output = None

    def __init__(self, parent=None):
        super(CreateWindow, self).__init__(parent)
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

        self.tgtfileLabel  = QtGui.QLabel('Target file name')
        self.tgtfileBtn    = QtGui.QPushButton('Select')
        self.tgtfileBtn.clicked.connect(self.selectTargetFilename)

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
        grid1.addWidget(self.tgtfileLabel, 4, 0)
        grid1.addWidget(self.tgtfileBtn,   4, 1)
        group1 = QtGui.QGroupBox('Source Configuration')
        group1.setLayout(grid1)

        self.runBtn = QtGui.QPushButton('Create dataset')
        self.runBtn.clicked.connect(self.run)

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.runBtn)

        centralWidget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(centralWidget)
        vbox.addStretch(1)
        vbox.addWidget(group1)
        vbox.addLayout(hbox1)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle('Create Dataset')
        self.statusBar().showMessage('Ready')
        self.show()

    def selectSourceDirectory(self):
        _dir = QtGui.QFileDialog.getExistingDirectory(self, caption="Select source directory")
        if _dir != '':
            self._dir = _dir
            self.statusBar().showMessage('{} directory selected.'.format(os.path.basename(self._dir)))

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
        result = []
        for fn in os.listdir(self._dir):
            fn = os.path.normcase(fn)
            if match(fn) is not None:
                result.append(os.path.join(self._dir, fn))
        return sorted(result)

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
            self.progress = QtGui.QProgressDialog("Progress","Cancel",0,len(images)-1)
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


def _findtiff(path, prefix):
    return sorted([p for p in path.iterdir() if p.match(prefix.strip()+'*') and (p.suffix.lower() in ['.tif', '.tiff'])])


def start_create(args):
    path = Path(args.path)
    images = _findtiff(path, args.image_prefix)
    bgnds = _findtiff(path, args.background_prefix) if args.background_prefix != None else []
    darks = _findtiff(path, args.dark_prefix) if args.dark_prefix != None else []
    # TODO: dataset.create will accept pathlib
    images = [str(im) for im in images]
    bgnds = [str(im) for im in bgnds]
    darks = [str(im) for im in darks]
    for i, name in dataset.create(args.output, images, bgnds, darks):
        print(i, name)


def start_createqt(args):
    app = QtGui.QApplication(sys.argv)
    win = CreateWindow()
    win.show()
    win.activateWindow()
    win.raise_()
    sys.exit(app.exec_())
