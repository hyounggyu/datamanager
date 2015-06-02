# -*- coding: utf-8 -*-

import os
import sys
import getopt

from PyQt4 import QtGui

from progress import ProgressWindow
from view import ViewWindow


class MainWindow(QtGui.QMainWindow):

    def __init__(self, dataset=None, parent=None):
        super(MainWindow, self).__init__(parent)
        self.dataset = dataset
        self.initUI()

    def initUI(self):
        newDatasetBtn    = QtGui.QPushButton('New')

        centralWidget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(centralWidget)
        vbox.addStretch(1)
        vbox.addWidget(newDatasetBtn)

        self.setCentralWidget(centralWidget)

        self.statusBar().showMessage('Ready')

    def open(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, caption='Select file')

    def view(self):
        ImageViewWindow(data, parent=self)


class App(QtGui.QApplication):

    def __init__(self, *argv):
        QtGui.QApplication.__init__(self, *argv)
        self.main = MainWindow()
        self.lastWindowClosed.connect(self.bye)
        self.main.show()
        self.main.activateWindow()
        self.main.raise_()

    def bye(self):
        self.exit(0)


def usage():
    print("""command -i sample.h5""")


def main():
    global app, dataset
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:', ['help', 'input='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-i', '--input'):
            try:
                dataset = Dataset(a)
            except OSError as err:
                print(err)
                sys.exit(2)
        else:
            pass

    app = App(sys.argv)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
