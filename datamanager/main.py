# -*- coding: utf-8 -*-

import os
import sys
import getopt

from PyQt4 import QtGui

from view import ViewWindow
from new import NewWindow
from config import ConfigWindow


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        newDatasetBtn = QtGui.QPushButton('New Dataset')
        newDatasetBtn.clicked.connect(self.new)

        viewDatasetBtn = QtGui.QPushButton('View Dataset')
        viewDatasetBtn.clicked.connect(self.view)

        #configBtn = QtGui.QPushButton('Config')
        #configBtn.clicked.connect(self.config)

        centralWidget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(centralWidget)
        vbox.addStretch(1)
        vbox.addWidget(newDatasetBtn)
        vbox.addWidget(viewDatasetBtn)
        vbox.addWidget(configBtn)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle('XNI Data Manager')
        self.statusBar().showMessage('Ready')

    def new(self):
        NewWindow(parent=self)

    def view(self):
        ViewWindow(parent=self)

    #def config(self):
    #    ConfigWindow(parent=self)


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
    print('''Usage: TODO:''')


def main():
    global app, dataset
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        else:
            pass

    app = App(sys.argv)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
