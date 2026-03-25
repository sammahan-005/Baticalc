# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        if not LoginWindow.objectName():
            LoginWindow.setObjectName(u"LoginWindow")
        LoginWindow.resize(480, 520)
        self.centralwidget = QWidget(LoginWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_title)

        self.label_subtitle = QLabel(self.centralwidget)
        self.label_subtitle.setObjectName(u"label_subtitle")
        self.label_subtitle.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_subtitle)

        self.label_email = QLabel(self.centralwidget)
        self.label_email.setObjectName(u"label_email")

        self.verticalLayout.addWidget(self.label_email)

        self.input_email = QLineEdit(self.centralwidget)
        self.input_email.setObjectName(u"input_email")
        self.input_email.setMinimumSize(QSize(0, 45))

        self.verticalLayout.addWidget(self.input_email)

        self.label_password = QLabel(self.centralwidget)
        self.label_password.setObjectName(u"label_password")

        self.verticalLayout.addWidget(self.label_password)

        self.input_password = QLineEdit(self.centralwidget)
        self.input_password.setObjectName(u"input_password")
        self.input_password.setMinimumSize(QSize(0, 45))
        self.input_password.setEchoMode(QLineEdit.Password)

        self.verticalLayout.addWidget(self.input_password)

        self.label_error = QLabel(self.centralwidget)
        self.label_error.setObjectName(u"label_error")
        self.label_error.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_error)

        self.btn_login = QPushButton(self.centralwidget)
        self.btn_login.setObjectName(u"btn_login")
        self.btn_login.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.btn_login)

        self.label_sep = QLabel(self.centralwidget)
        self.label_sep.setObjectName(u"label_sep")
        self.label_sep.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_sep)

        self.btn_goto_register = QPushButton(self.centralwidget)
        self.btn_goto_register.setObjectName(u"btn_goto_register")
        self.btn_goto_register.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.btn_goto_register)

        self.btn_back = QPushButton(self.centralwidget)
        self.btn_back.setObjectName(u"btn_back")
        self.btn_back.setMinimumSize(QSize(0, 35))

        self.verticalLayout.addWidget(self.btn_back)

        LoginWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoginWindow)

        QMetaObject.connectSlotsByName(LoginWindow)
    # setupUi

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(QCoreApplication.translate("LoginWindow", u"BATICALC - Connexion", None))
        self.label_title.setText(QCoreApplication.translate("LoginWindow", u"<h1>BATICALC</h1>", None))
        self.label_subtitle.setText(QCoreApplication.translate("LoginWindow", u"Connexion a votre compte", None))
        self.label_email.setText(QCoreApplication.translate("LoginWindow", u"Email", None))
        self.input_email.setPlaceholderText(QCoreApplication.translate("LoginWindow", u"Entrez votre email", None))
        self.label_password.setText(QCoreApplication.translate("LoginWindow", u"Mot de passe", None))
        self.input_password.setPlaceholderText(QCoreApplication.translate("LoginWindow", u"Entrez votre mot de passe", None))
        self.label_error.setText("")
        self.btn_login.setText(QCoreApplication.translate("LoginWindow", u"Se connecter", None))
        self.label_sep.setText(QCoreApplication.translate("LoginWindow", u"Pas encore de compte ?", None))
        self.btn_goto_register.setText(QCoreApplication.translate("LoginWindow", u"Creer un compte", None))
        self.btn_back.setText(QCoreApplication.translate("LoginWindow", u"Retour", None))
    # retranslateUi

