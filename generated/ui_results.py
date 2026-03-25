# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'results.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QTableWidget,
    QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget)

class Ui_ResultsWindow(object):
    def setupUi(self, ResultsWindow):
        if not ResultsWindow.objectName():
            ResultsWindow.setObjectName(u"ResultsWindow")
        ResultsWindow.resize(1100, 750)
        self.centralwidget = QWidget(ResultsWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.headerBar = QWidget(self.centralwidget)
        self.headerBar.setObjectName(u"headerBar")
        self.headerBar.setMinimumSize(QSize(0, 70))
        self.headerLayout = QHBoxLayout(self.headerBar)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(0, 0, 0, 0)
        self.label_titre = QLabel(self.headerBar)
        self.label_titre.setObjectName(u"label_titre")

        self.headerLayout.addWidget(self.label_titre)

        self.spacerItem = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.spacerItem)

        self.label_nom_projet = QLabel(self.headerBar)
        self.label_nom_projet.setObjectName(u"label_nom_projet")

        self.headerLayout.addWidget(self.label_nom_projet)

        self.btn_exporter_pdf = QPushButton(self.headerBar)
        self.btn_exporter_pdf.setObjectName(u"btn_exporter_pdf")
        self.btn_exporter_pdf.setMinimumSize(QSize(180, 45))

        self.headerLayout.addWidget(self.btn_exporter_pdf)

        self.btn_retour = QPushButton(self.headerBar)
        self.btn_retour.setObjectName(u"btn_retour")
        self.btn_retour.setMinimumSize(QSize(120, 45))

        self.headerLayout.addWidget(self.btn_retour)


        self.mainLayout.addWidget(self.headerBar)

        self.statsBar = QWidget(self.centralwidget)
        self.statsBar.setObjectName(u"statsBar")
        self.statsBar.setMinimumSize(QSize(0, 90))
        self.statsLayout = QHBoxLayout(self.statsBar)
        self.statsLayout.setObjectName(u"statsLayout")
        self.statsLayout.setContentsMargins(0, 0, 0, 0)
        self.stat_murs = QFrame(self.statsBar)
        self.stat_murs.setObjectName(u"stat_murs")
        self.stat_murs.setFrameShape(QFrame.StyledPanel)
        self.vboxLayout = QVBoxLayout(self.stat_murs)
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.label_nb_murs = QLabel(self.stat_murs)
        self.label_nb_murs.setObjectName(u"label_nb_murs")
        self.label_nb_murs.setAlignment(Qt.AlignCenter)

        self.vboxLayout.addWidget(self.label_nb_murs)

        self.label_nb_murs_txt = QLabel(self.stat_murs)
        self.label_nb_murs_txt.setObjectName(u"label_nb_murs_txt")
        self.label_nb_murs_txt.setAlignment(Qt.AlignCenter)

        self.vboxLayout.addWidget(self.label_nb_murs_txt)


        self.statsLayout.addWidget(self.stat_murs)

        self.stat_fondations = QFrame(self.statsBar)
        self.stat_fondations.setObjectName(u"stat_fondations")
        self.stat_fondations.setFrameShape(QFrame.StyledPanel)
        self.vboxLayout1 = QVBoxLayout(self.stat_fondations)
        self.vboxLayout1.setObjectName(u"vboxLayout1")
        self.label_nb_fondations = QLabel(self.stat_fondations)
        self.label_nb_fondations.setObjectName(u"label_nb_fondations")
        self.label_nb_fondations.setAlignment(Qt.AlignCenter)

        self.vboxLayout1.addWidget(self.label_nb_fondations)

        self.label_nb_fondations_txt = QLabel(self.stat_fondations)
        self.label_nb_fondations_txt.setObjectName(u"label_nb_fondations_txt")
        self.label_nb_fondations_txt.setAlignment(Qt.AlignCenter)

        self.vboxLayout1.addWidget(self.label_nb_fondations_txt)


        self.statsLayout.addWidget(self.stat_fondations)

        self.stat_poteaux = QFrame(self.statsBar)
        self.stat_poteaux.setObjectName(u"stat_poteaux")
        self.stat_poteaux.setFrameShape(QFrame.StyledPanel)
        self.vboxLayout2 = QVBoxLayout(self.stat_poteaux)
        self.vboxLayout2.setObjectName(u"vboxLayout2")
        self.label_nb_poteaux = QLabel(self.stat_poteaux)
        self.label_nb_poteaux.setObjectName(u"label_nb_poteaux")
        self.label_nb_poteaux.setAlignment(Qt.AlignCenter)

        self.vboxLayout2.addWidget(self.label_nb_poteaux)

        self.label_nb_poteaux_txt = QLabel(self.stat_poteaux)
        self.label_nb_poteaux_txt.setObjectName(u"label_nb_poteaux_txt")
        self.label_nb_poteaux_txt.setAlignment(Qt.AlignCenter)

        self.vboxLayout2.addWidget(self.label_nb_poteaux_txt)


        self.statsLayout.addWidget(self.stat_poteaux)

        self.stat_toitures = QFrame(self.statsBar)
        self.stat_toitures.setObjectName(u"stat_toitures")
        self.stat_toitures.setFrameShape(QFrame.StyledPanel)
        self.vboxLayout3 = QVBoxLayout(self.stat_toitures)
        self.vboxLayout3.setObjectName(u"vboxLayout3")
        self.label_nb_toitures = QLabel(self.stat_toitures)
        self.label_nb_toitures.setObjectName(u"label_nb_toitures")
        self.label_nb_toitures.setAlignment(Qt.AlignCenter)

        self.vboxLayout3.addWidget(self.label_nb_toitures)

        self.label_nb_toitures_txt = QLabel(self.stat_toitures)
        self.label_nb_toitures_txt.setObjectName(u"label_nb_toitures_txt")
        self.label_nb_toitures_txt.setAlignment(Qt.AlignCenter)

        self.vboxLayout3.addWidget(self.label_nb_toitures_txt)


        self.statsLayout.addWidget(self.stat_toitures)


        self.mainLayout.addWidget(self.statsBar)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_murs = QWidget()
        self.tab_murs.setObjectName(u"tab_murs")
        self.murLayout = QVBoxLayout(self.tab_murs)
        self.murLayout.setObjectName(u"murLayout")
        self.table_murs = QTableWidget(self.tab_murs)
        self.table_murs.setObjectName(u"table_murs")
        self.table_murs.setColumnCount(6)
        self.table_murs.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_murs.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_murs.setAlternatingRowColors(True)

        self.murLayout.addWidget(self.table_murs)

        self.tabWidget.addTab(self.tab_murs, "")
        self.tab_fondations = QWidget()
        self.tab_fondations.setObjectName(u"tab_fondations")
        self.fondLayout = QVBoxLayout(self.tab_fondations)
        self.fondLayout.setObjectName(u"fondLayout")
        self.table_fondations = QTableWidget(self.tab_fondations)
        self.table_fondations.setObjectName(u"table_fondations")
        self.table_fondations.setColumnCount(6)
        self.table_fondations.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_fondations.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_fondations.setAlternatingRowColors(True)

        self.fondLayout.addWidget(self.table_fondations)

        self.tabWidget.addTab(self.tab_fondations, "")
        self.tab_poteaux = QWidget()
        self.tab_poteaux.setObjectName(u"tab_poteaux")
        self.poteauxLayout = QVBoxLayout(self.tab_poteaux)
        self.poteauxLayout.setObjectName(u"poteauxLayout")
        self.table_poteaux = QTableWidget(self.tab_poteaux)
        self.table_poteaux.setObjectName(u"table_poteaux")
        self.table_poteaux.setColumnCount(6)
        self.table_poteaux.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_poteaux.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_poteaux.setAlternatingRowColors(True)

        self.poteauxLayout.addWidget(self.table_poteaux)

        self.tabWidget.addTab(self.tab_poteaux, "")
        self.tab_toitures = QWidget()
        self.tab_toitures.setObjectName(u"tab_toitures")
        self.toitLayout = QVBoxLayout(self.tab_toitures)
        self.toitLayout.setObjectName(u"toitLayout")
        self.table_toitures = QTableWidget(self.tab_toitures)
        self.table_toitures.setObjectName(u"table_toitures")
        self.table_toitures.setColumnCount(5)
        self.table_toitures.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_toitures.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_toitures.setAlternatingRowColors(True)

        self.toitLayout.addWidget(self.table_toitures)

        self.tabWidget.addTab(self.tab_toitures, "")
        self.tab_erreurs = QWidget()
        self.tab_erreurs.setObjectName(u"tab_erreurs")
        self.errLayout = QVBoxLayout(self.tab_erreurs)
        self.errLayout.setObjectName(u"errLayout")
        self.text_erreurs = QTextEdit(self.tab_erreurs)
        self.text_erreurs.setObjectName(u"text_erreurs")
        self.text_erreurs.setReadOnly(True)

        self.errLayout.addWidget(self.text_erreurs)

        self.tabWidget.addTab(self.tab_erreurs, "")

        self.mainLayout.addWidget(self.tabWidget)

        ResultsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ResultsWindow)

        QMetaObject.connectSlotsByName(ResultsWindow)
    # setupUi

    def retranslateUi(self, ResultsWindow):
        ResultsWindow.setWindowTitle(QCoreApplication.translate("ResultsWindow", u"BATICALC - Resultats", None))
        self.label_titre.setText(QCoreApplication.translate("ResultsWindow", u"Resultats d'analyse IFC", None))
        self.label_nom_projet.setText(QCoreApplication.translate("ResultsWindow", u"Projet", None))
        self.btn_exporter_pdf.setText(QCoreApplication.translate("ResultsWindow", u"Telecharger PDF", None))
        self.btn_retour.setText(QCoreApplication.translate("ResultsWindow", u"Retour", None))
        self.label_nb_murs.setText(QCoreApplication.translate("ResultsWindow", u"0", None))
        self.label_nb_murs_txt.setText(QCoreApplication.translate("ResultsWindow", u"Murs", None))
        self.label_nb_fondations.setText(QCoreApplication.translate("ResultsWindow", u"0", None))
        self.label_nb_fondations_txt.setText(QCoreApplication.translate("ResultsWindow", u"Fondations", None))
        self.label_nb_poteaux.setText(QCoreApplication.translate("ResultsWindow", u"0", None))
        self.label_nb_poteaux_txt.setText(QCoreApplication.translate("ResultsWindow", u"Poteaux", None))
        self.label_nb_toitures.setText(QCoreApplication.translate("ResultsWindow", u"0", None))
        self.label_nb_toitures_txt.setText(QCoreApplication.translate("ResultsWindow", u"Toitures", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_murs), QCoreApplication.translate("ResultsWindow", u"Murs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_fondations), QCoreApplication.translate("ResultsWindow", u"Fondations", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_poteaux), QCoreApplication.translate("ResultsWindow", u"Poteaux", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_toitures), QCoreApplication.translate("ResultsWindow", u"Toitures", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_erreurs), QCoreApplication.translate("ResultsWindow", u"Avertissements", None))
    # retranslateUi

