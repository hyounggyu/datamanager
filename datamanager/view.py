import numpy as np
import h5py
from PyQt4 import QtGui
import pyqtgraph as pg

from xni.io import dataset

class ViewWindow(QtGui.QMainWindow):

    #image = None

    def __init__(self, image, parent=None):
        super(ViewWindow, self).__init__(parent)
        imv = pg.ImageView()
        imv.setImage(image)
        self.setCentralWidget(imv)
        self.setWindowTitle('ImageView')
        self.show()

    #def open(self):
    #    fname = QtGui.QFileDialog.getOpenFileName(self, caption='Select file')
    #    if fname == '':
    #        self.warning('File does not selected')
    #        return
    #    f = h5py.File(fname, 'r')
    #    dset = f['original/images'] # TODO: selectable
    #    arr = np.zeros(dset.shape, dtype=dset.dtype)
    #    dset.read_direct(arr)
    #    self.image = arr
    #    self.initUI()

    #def warning(self, msg):
    #    msgbox = QtGui.QMessageBox(self)
    #    msgbox.setText(msg)
    #    msgbox.exec_()

def start_view(args):
    dset = None
    app = QtGui.QApplication(sys.argv)
    win = ViewWindow(dset)
    sys.exit(app.exec_())

def start_removeview(args):
    dset = dataset.recv()
    app = QtGui.QApplication(sys.argv)
    win = ViewWindow(dset)
    sys.exit(app.exec_())
