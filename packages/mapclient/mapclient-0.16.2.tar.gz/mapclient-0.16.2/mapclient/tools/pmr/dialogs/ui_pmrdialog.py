# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pmrdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from mapclient.tools.pmr.widgets.searchwidget import SearchWidget
from mapclient.tools.pmr.widgets.settingswidget import SettingsWidget


class Ui_PMRDialog(object):
    def setupUi(self, PMRDialog):
        if not PMRDialog.objectName():
            PMRDialog.setObjectName(u"PMRDialog")
        PMRDialog.resize(433, 489)
        self.verticalLayout = QVBoxLayout(PMRDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(PMRDialog)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.loginStackedWidget = QStackedWidget(PMRDialog)
        self.loginStackedWidget.setObjectName(u"loginStackedWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.loginStackedWidget.sizePolicy().hasHeightForWidth())
        self.loginStackedWidget.setSizePolicy(sizePolicy1)
        self.loginStackedWidget.setMaximumSize(QSize(16777215, 40))
        self.loginPage = QWidget()
        self.loginPage.setObjectName(u"loginPage")
        self.horizontalLayout_2 = QHBoxLayout(self.loginPage)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.registerLabel = QLabel(self.loginPage)
        self.registerLabel.setObjectName(u"registerLabel")
        font = QFont()
        font.setPointSize(7)
        self.registerLabel.setFont(font)
        self.registerLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.registerLabel)

        self.loginStackedWidget.addWidget(self.loginPage)
        self.logoutPage = QWidget()
        self.logoutPage.setObjectName(u"logoutPage")
        self.horizontalLayout_3 = QHBoxLayout(self.logoutPage)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.deregisterLabel = QLabel(self.logoutPage)
        self.deregisterLabel.setObjectName(u"deregisterLabel")
        self.deregisterLabel.setFont(font)
        self.deregisterLabel.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.deregisterLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.deregisterLabel)

        self.loginStackedWidget.addWidget(self.logoutPage)
        self.inactivePage = QWidget()
        self.inactivePage.setObjectName(u"inactivePage")
        self.horizontalLayout_6 = QHBoxLayout(self.inactivePage)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.inactiveLabel = QLabel(self.inactivePage)
        self.inactiveLabel.setObjectName(u"inactiveLabel")
        self.inactiveLabel.setFont(font)

        self.horizontalLayout_6.addWidget(self.inactiveLabel)

        self.loginStackedWidget.addWidget(self.inactivePage)

        self.horizontalLayout.addWidget(self.loginStackedWidget)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tabWidget = QTabWidget(PMRDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy2)
        self.searchTab = QWidget()
        self.searchTab.setObjectName(u"searchTab")
        self.horizontalLayout_4 = QHBoxLayout(self.searchTab)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.searchWidget = SearchWidget(self.searchTab)
        self.searchWidget.setObjectName(u"searchWidget")

        self.horizontalLayout_4.addWidget(self.searchWidget)

        self.tabWidget.addTab(self.searchTab, "")
        self.settingsTab = QWidget()
        self.settingsTab.setObjectName(u"settingsTab")
        self.horizontalLayout_5 = QHBoxLayout(self.settingsTab)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.settingsWidget = SettingsWidget(self.settingsTab)
        self.settingsWidget.setObjectName(u"settingsWidget")

        self.horizontalLayout_5.addWidget(self.settingsWidget)

        self.tabWidget.addTab(self.settingsTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(PMRDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(PMRDialog)
        self.buttonBox.accepted.connect(PMRDialog.accept)
        self.buttonBox.rejected.connect(PMRDialog.reject)

        self.loginStackedWidget.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PMRDialog)
    # setupUi

    def retranslateUi(self, PMRDialog):
        PMRDialog.setWindowTitle(QCoreApplication.translate("PMRDialog", u"PMR", None))
        self.label.setText(QCoreApplication.translate("PMRDialog", u"Physiome Model Repository", None))
        self.registerLabel.setText(QCoreApplication.translate("PMRDialog", u"<a href=\"mapclient.register\">register</a>", None))
        self.deregisterLabel.setText(QCoreApplication.translate("PMRDialog", u"<a href=\"http://mapclient.logout\">deregister</a>", None))
#if QT_CONFIG(tooltip)
        self.inactiveLabel.setToolTip(QCoreApplication.translate("PMRDialog", u"No Physiome Model Repository currently set as active", None))
#endif // QT_CONFIG(tooltip)
        self.inactiveLabel.setText(QCoreApplication.translate("PMRDialog", u"inactive", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.searchTab), QCoreApplication.translate("PMRDialog", u"Search", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), QCoreApplication.translate("PMRDialog", u"Settings", None))
    # retranslateUi

