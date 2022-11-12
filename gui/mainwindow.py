# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowHzvZpr.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import *
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

from PySide6.Qt3DCore import (Qt3DCore)
from PySide6.Qt3DExtras import (Qt3DExtras)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(660, 540)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionQuit.setCheckable(True)
        self.actionQuit.setShortcutVisibleInContextMenu(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 661, 491))
        self.layout_main = QVBoxLayout(self.verticalLayoutWidget)
        self.layout_main.setObjectName(u"layout_main")
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.sim_window = Qt3DExtras.Qt3DWindow() #QOpenGLWidget(self.verticalLayoutWidget)
        self.sim_window.setObjectName(u"sim_window")

        self.layout_main.addWidget(self.sim_window)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 660, 24))
        self.menuSimulator = QMenu(self.menubar)
        self.menuSimulator.setObjectName(u"menuSimulator")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuSimulator.menuAction())
        self.menuSimulator.addAction(self.actionQuit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Evolving Robot Simulator", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.menuSimulator.setTitle(QCoreApplication.translate("MainWindow", u"Simulator", None))
    # retranslateUi
