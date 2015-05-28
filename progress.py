# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore


class ProgressWindow(QtGui.QMainWindow):

    step = 0

    def __init__(self, async_result, parent=None):
        super(ProgressWindow, self).__init__(parent)
        self.parent = parent
        self.ar = async_result
        self.initUI()

    def initUI(self):
        # 여기에 기본 UI를 추가해야한다.
        self.stopButton.clicked.connect(self.stop)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)
        self.parent.setEnabled(False)
        self.setEnabled(True)
        self.show()

    def timerEvent(self):
        if self.step >= 100.0:
            self.timer.stop()
            self.dataset.update()
            self.parent.setEnabled(True)
            self.close()
            return
        self.step = 100.0 * self.ar.progress / len(self.ar)
        self.progressBar.setValue(self.step)

    def stop(self):
        self.timer.stop()
        self.ar.abort()
        self.parent.setEnabled(True)
        self.close()
