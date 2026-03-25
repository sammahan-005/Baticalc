# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register.ui'
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

class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        if not RegisterWindow.objectName():
            RegisterWindow.setObjectName(u"RegisterWindow")
        RegisterWindow.resize(480, 620)
        self.centralwidget = QWidget(RegisterWindow)
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

        self.label_nom = QLabel(self.centralwidget)
        self.label_nom.setObjectName(u"label_nom")

        self.verticalLayout.addWidget(self.label_nom)

        self.input_nom = QLineEdit(self.centralwidget)
        self.input_nom.setObjectName(u"input_nom")
        self.input_nom.setMinimumSize(QSize(0, 45))

        self.verticalLayout.addWidget(self.input_nom)

        self.label_email = QLabel(self.centralwidget)
        self.label_email.setObjectName(u"label_email")

        self.verticalLayout.addWidget(self.label_email)

        self.input_email = QLineEdit(self.centralwidget)
        self.input_email.setObjectName(u"input_email")
        self.input_email.setMinimumSize(QSize(0, 45))

        self.verticalLayout.addWidget(self.input_email)

        self.label_mdp = QLabel(self.centralwidget)
        self.label_mdp.setObjectName(u"label_mdp")

        self.verticalLayout.addWidget(self.label_mdp)

        self.input_mdp = QLineEdit(self.centralwidget)
        self.input_mdp.setObjectName(u"input_mdp")
        self.input_mdp.setMinimumSize(QSize(0, 45))
        self.input_mdp.setEchoMode(QLineEdit.Password)

        self.verticalLayout.addWidget(self.input_mdp)

        self.label_confirm = QLabel(self.centralwidget)
        self.label_confirm.setObjectName(u"label_confirm")

        self.verticalLayout.addWidget(self.label_confirm)

        self.input_confirm = QLineEdit(self.centralwidget)
        self.input_confirm.setObjectName(u"input_confirm")
        self.input_confirm.setMinimumSize(QSize(0, 45))
        self.input_confirm.setEchoMode(QLineEdit.Password)

        self.verticalLayout.addWidget(self.input_confirm)

        self.label_error = QLabel(self.centralwidget)
        self.label_error.setObjectName(u"label_error")
        self.label_error.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_error)

        self.btn_register = QPushButton(self.centralwidget)
        self.btn_register.setObjectName(u"btn_register")
        self.btn_register.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.btn_register)

        self.label_sep = QLabel(self.centralwidget)
        self.label_sep.setObjectName(u"label_sep")
        self.label_sep.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_sep)

        self.btn_goto_login = QPushButton(self.centralwidget)
        self.btn_goto_login.setObjectName(u"btn_goto_login")
        self.btn_goto_login.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.btn_goto_login)

        self.btn_back = QPushButton(self.centralwidget)
        self.btn_back.setObjectName(u"btn_back")
        self.btn_back.setMinimumSize(QSize(0, 35))

        self.verticalLayout.addWidget(self.btn_back)

        RegisterWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RegisterWindow)

        QMetaObject.connectSlotsByName(RegisterWindow)
    # setupUi

    def retranslateUi(self, RegisterWindow):
        RegisterWindow.setWindowTitle(QCoreApplication.translate("RegisterWindow", u"BATICALC - Inscription", None))
        self.label_title.setText(QCoreApplication.translate("RegisterWindow", u"<h1>BATICALC</h1>", None))
        self.label_subtitle.setText(QCoreApplication.translate("RegisterWindow", u"Creer votre compte", None))
        self.label_nom.setText(QCoreApplication.translate("RegisterWindow", u"Nom complet", None))
        self.input_nom.setPlaceholderText(QCoreApplication.translate("RegisterWindow", u"Entrez votre nom complet", None))
        self.label_email.setText(QCoreApplication.translate("RegisterWindow", u"Email", None))
        self.input_email.setPlaceholderText(QCoreApplication.translate("RegisterWindow", u"Entrez votre email", None))
        self.label_mdp.setText(QCoreApplication.translate("RegisterWindow", u"Mot de passe", None))
        self.input_mdp.setPlaceholderText(QCoreApplication.translate("RegisterWindow", u"Entrez votre mot de passe", None))
        self.label_confirm.setText(QCoreApplication.translate("RegisterWindow", u"Confirmer le mot de passe", None))
        self.input_confirm.setPlaceholderText(QCoreApplication.translate("RegisterWindow", u"Confirmez votre mot de passe", None))
        self.label_error.setText("")
        self.btn_register.setText(QCoreApplication.translate("RegisterWindow", u"Creer mon compte", None))
        self.label_sep.setText(QCoreApplication.translate("RegisterWindow", u"Vous avez deja un compte ?", None))
        self.btn_goto_login.setText(QCoreApplication.translate("RegisterWindow", u"Se connecter", None))
        self.btn_back.setText(QCoreApplication.translate("RegisterWindow", u"Retour", None))
    # retranslateUi

