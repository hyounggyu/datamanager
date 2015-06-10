from PyQt4 import QtGui

class ConfigWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(ConfigWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        prefixLabel  = QtGui.QLabel('Image file prefix')
        bgndprefixLabel = QtGui.QLabel('Background image file prefix')
        darkprefixLabel = QtGui.QLabel('Dark image file prefix')

        srcdirEdit   = QtGui.QLineEdit()
        prefixEdit   = QtGui.QLineEdit()
        bgndprefixEdit  = QtGui.QLineEdit()
        darkprefixEdit  = QtGui.QLineEdit()

        okBtn = QtGui.QPushButton('Ok')
        cancelBtn  = QtGui.QPushButton('Cancel')

        grid1 = QtGui.QGridLayout()
        grid1.setSpacing(10)
        grid1.addWidget(prefixLabel,     0, 0)
        grid1.addWidget(prefixEdit,      0, 1)
        grid1.addWidget(bgndprefixLabel, 1, 0)
        grid1.addWidget(bgndprefixEdit,  1, 1)
        grid1.addWidget(darkprefixLabel, 2, 0)
        grid1.addWidget(darkprefixEdit,  2, 1)
        group1 = QtGui.QGroupBox('Default Prefix')
        group1.setLayout(grid1)

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(okBtn)
        hbox1.addWidget(cancelBtn)

        centralWidget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(centralWidget)
        vbox.addStretch(1)
        vbox.addWidget(group1)
        vbox.addLayout(hbox1)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle('Configuration')
        self.statusBar().showMessage('Ready')
        self.show()
