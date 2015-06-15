from PyQt4 import QtGui
import pyqtgraph as pg

import numpy as np


def swap(im):
    if im.ndim == 2:
        return np.swapaxes(im, 0, 1)
    elif im.ndim == 3:
        return np.swapaxes(im, 1, 2)
    else:
        return None


class ViewWindow(QtGui.QMainWindow):

    image = None

    def __init__(self, parent=None):
        super(ViewWindow, self).__init__(parent)

        filename = QtGui.QFileDialog.getOpenFileName(self, caption='Select file')
        if filename == '':
            self.warning('File does not selected')
            return
        else
            self.openfile(filename)
            self.initUI()

    def initUI(self):
        pass
        # TODO:
        #imv = pg.ImageView()
        #imv.setImage(swap(self.image))
        #self.setCentralWidget(imv)
        #self.setWindowTitle('ImageView')
        #self.show()

    def openfile(self):
        pass
        # TODO:
        #self.image = image

    def warning(self, msg):
        msgbox = QtGui.QMessageBox(self)
        msgbox.setText(msg)
        msgbox.exec_()
