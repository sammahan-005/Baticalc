# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'welcome.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_WelcomeWindow(object):
    def setupUi(self, WelcomeWindow):
        if not WelcomeWindow.objectName():
            WelcomeWindow.setObjectName(u"WelcomeWindow")
        WelcomeWindow.resize(800, 600)
        self.centralwidget = QWidget(WelcomeWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.sp_top = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.sp_top)

        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_title)

        self.label_subtitle = QLabel(self.centralwidget)
        self.label_subtitle.setObjectName(u"label_subtitle")
        self.label_subtitle.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_subtitle)

        self.label_desc = QLabel(self.centralwidget)
        self.label_desc.setObjectName(u"label_desc")
        self.label_desc.setWordWrap(True)
        self.label_desc.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_desc)

        self.btnLayout = QHBoxLayout()
        self.btnLayout.setObjectName(u"btnLayout")
        self.sp_l = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.btnLayout.addItem(self.sp_l)

        self.btn_login = QPushButton(self.centralwidget)
        self.btn_login.setObjectName(u"btn_login")
        self.btn_login.setMinimumSize(QSize(200, 50))

        self.btnLayout.addWidget(self.btn_login)

        self.btn_register = QPushButton(self.centralwidget)
        self.btn_register.setObjectName(u"btn_register")
        self.btn_register.setMinimumSize(QSize(200, 50))

        self.btnLayout.addWidget(self.btn_register)

        self.sp_r = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.btnLayout.addItem(self.sp_r)


        self.verticalLayout.addLayout(self.btnLayout)

        self.sp_bot = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.sp_bot)

        WelcomeWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(WelcomeWindow)

        QMetaObject.connectSlotsByName(WelcomeWindow)
    # setupUi

    def retranslateUi(self, WelcomeWindow):
        WelcomeWindow.setWindowTitle(QCoreApplication.translate("WelcomeWindow", u"BATICALC - Bienvenue", None))
        self.label_title.setText(QCoreApplication.translate("WelcomeWindow", u"<h1>BATICALC</h1>", None))
        self.label_subtitle.setText(QCoreApplication.translate("WelcomeWindow", u"Calculateur BIM pour Gros Oeuvre", None))
        self.label_desc.setText(QCoreApplication.translate("WelcomeWindow", u"L'outil professionnel pour le calcul et l'estimation des ouvrages de gros oeuvre a partir de modeles IFC.", None))
        self.btn_login.setText(QCoreApplication.translate("WelcomeWindow", u"Se connecter", None))
        self.btn_register.setText(QCoreApplication.translate("WelcomeWindow", u"Creer un compte", None))
    # retranslateUi

