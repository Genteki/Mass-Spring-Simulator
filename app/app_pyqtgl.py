import sys, os
import numpy as np
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QThread, Signal)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import *

import pyqtgraph.opengl as gl
import pyqtgraph as pg


import json
config = json.load(open('config.json'))
projPath = config["project_path"]
print(os.getcwd())
sys.path.append(os.getcwd())

from gui.mainwindow_pyqtgl import *

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setup_action()
        self.setup_glwindow()

    def setup_action(self):
        self.actionQuit.triggered.connect(self.close)

    def setup_glwindow(self):
        gx = gl.GLGridItem(); gx.rotate(90, 0, 1, 0)
        gy = gl.GLGridItem(); gx.rotate(90, 1, 0, 0)
        gz = gl.GLGridItem()
        #self.gl_window.addItem(gx)
        #self.gl_window.addItem(gy)
        self.gl_window.addItem(gz)
        self.gl_window.show()

        pos = np.empty((8, 3))
        size = np.empty((8))
        color = np.empty((8, 4))
        # draw vertices
        s = .5; c = (1,1,1,.7)
        pos[0] = (0,0,0); pos[1] = (0,1,0); pos[2] = (1,0,0); pos[3] = (1,1,0)
        pos[4] = (0,0,1); pos[5] = (0,1,1); pos[6] = (1,0,1); pos[7] = (1,1,1)
        for i in range(8):
            size[i] = s
            color[i] = c

        # draw springs
        pos_pair = np.array([
            pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7],
            pos[0], pos[2], pos[1], pos[3], pos[4], pos[6], pos[5], pos[7],
            pos[0], pos[4], pos[1], pos[5], pos[2], pos[6], pos[3], pos[7]
            ])
        lines = gl.GLLinePlotItem(pos=pos_pair, color=c, width=3,mode="lines")
        lines.setShadowPen(QColor(18, 134, 3))


        sp1 = gl.GLScatterPlotItem(pos=pos, size=size, color=color, pxMode=False)
        sp1.translate(0,0,0)
        self.gl_window.addItem(sp1)
        self.gl_window.addItem(lines)



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
