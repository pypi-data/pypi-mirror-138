# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pluginprogress.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import resources_rc

class Ui_DownloadProgress(object):
    def setupUi(self, DownloadProgress):
        if not DownloadProgress.objectName():
            DownloadProgress.setObjectName(u"DownloadProgress")
        DownloadProgress.resize(300, 108)
        DownloadProgress.setMinimumSize(QSize(300, 90))
        DownloadProgress.setMaximumSize(QSize(300, 108))
        icon = QIcon()
        icon.addFile(u":/mapclient/images/icon-app.png", QSize(), QIcon.Normal, QIcon.Off)
        DownloadProgress.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(DownloadProgress)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(DownloadProgress)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.progressBar = QProgressBar(DownloadProgress)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.verticalLayout.addWidget(self.progressBar)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.cancelDownload = QPushButton(DownloadProgress)
        self.cancelDownload.setObjectName(u"cancelDownload")

        self.horizontalLayout.addWidget(self.cancelDownload)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(DownloadProgress)

        QMetaObject.connectSlotsByName(DownloadProgress)
    # setupUi

    def retranslateUi(self, DownloadProgress):
        DownloadProgress.setWindowTitle(QCoreApplication.translate("DownloadProgress", u"Loading Plugins", None))
        self.label.setText("")
        self.cancelDownload.setText(QCoreApplication.translate("DownloadProgress", u"Cancel", None))
    # retranslateUi

