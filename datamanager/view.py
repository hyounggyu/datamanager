import sys

import numpy as np
import h5py
from PyQt4 import QtGui
import pyqtgraph as pg

from xni.io import dataset


class ViewWindow(QtGui.QMainWindow):

    def __init__(self, data, parent=None):
        super(ViewWindow, self).__init__(parent)
        imv = pg.ImageView()
        imv.setImage(self._swap(data))
        self.setCentralWidget(imv)
        self.setWindowTitle('ImageView')
        self.show()

    def _swap(self, data):
        if data.ndim == 2:
            return np.swapaxes(data, 0, 1)
        elif data.ndim == 3:
            return np.swapaxes(data, 1, 2)
        else:
            return None


def start_view(args):
    group_name = 'original' if args.group == None else args.group
    dataset_name = 'images' if args.dataset == None else args.dataset
    data = dataset.load(args.filename, grp=group_name, dset=dataset_name)
    sys.exit(start(data))


def start_remoteview(args):
    ip = '127.0.0.1' if args.ip == None else args.ip
    port = '5550' if args.port == None else args.port
    if args.slice == None:
        slice = [0,1,1]
    else:
        slice = [int(x) for x in args.slice.split(':')]
    data = dataset.recv(_slice=slice, ip=ip, port=port)
    ret = start(data)
    dataset.bye(ip=ip, port=port)
    sys.exit(ret)

def start(data):
    app = QtGui.QApplication(sys.argv)
    win = ViewWindow(data)
    win.show()
    win.activateWindow()
    win.raise_()
    return app.exec_()
