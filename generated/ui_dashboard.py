# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dashboard.ui'
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
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_DashboardWindow(object):
    def setupUi(self, DashboardWindow):
        if not DashboardWindow.objectName():
            DashboardWindow.setObjectName(u"DashboardWindow")
        DashboardWindow.resize(1100, 720)
        self.centralwidget = QWidget(DashboardWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QHBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.sidebar = QWidget(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(220, 0))
        self.sidebar.setMaximumSize(QSize(220, 16777215))
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(0, 0, 0, 0)
        self.label_logo = QLabel(self.sidebar)
        self.label_logo.setObjectName(u"label_logo")
        self.label_logo.setAlignment(Qt.AlignCenter)
        self.label_logo.setMinimumSize(QSize(0, 70))

        self.sidebarLayout.addWidget(self.label_logo)

        self.label_user_name = QLabel(self.sidebar)
        self.label_user_name.setObjectName(u"label_user_name")
        self.label_user_name.setAlignment(Qt.AlignCenter)

        self.sidebarLayout.addWidget(self.label_user_name)

        self.btn_nav_dashboard = QPushButton(self.sidebar)
        self.btn_nav_dashboard.setObjectName(u"btn_nav_dashboard")
        self.btn_nav_dashboard.setMinimumSize(QSize(0, 50))
        self.btn_nav_dashboard.setCheckable(True)
        self.btn_nav_dashboard.setChecked(True)

        self.sidebarLayout.addWidget(self.btn_nav_dashboard)

        self.btn_nav_projets = QPushButton(self.sidebar)
        self.btn_nav_projets.setObjectName(u"btn_nav_projets")
        self.btn_nav_projets.setMinimumSize(QSize(0, 50))
        self.btn_nav_projets.setCheckable(True)

        self.sidebarLayout.addWidget(self.btn_nav_projets)

        self.btn_nav_nouveau = QPushButton(self.sidebar)
        self.btn_nav_nouveau.setObjectName(u"btn_nav_nouveau")
        self.btn_nav_nouveau.setMinimumSize(QSize(0, 50))
        self.btn_nav_nouveau.setCheckable(True)

        self.sidebarLayout.addWidget(self.btn_nav_nouveau)

        self.sp_side = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.sp_side)

        self.btn_deconnexion = QPushButton(self.sidebar)
        self.btn_deconnexion.setObjectName(u"btn_deconnexion")
        self.btn_deconnexion.setMinimumSize(QSize(0, 50))

        self.sidebarLayout.addWidget(self.btn_deconnexion)


        self.mainLayout.addWidget(self.sidebar)

        self.content_area = QWidget(self.centralwidget)
        self.content_area.setObjectName(u"content_area")
        self.contentLayout = QVBoxLayout(self.content_area)
        self.contentLayout.setObjectName(u"contentLayout")
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.topBar = QHBoxLayout()
        self.topBar.setObjectName(u"topBar")
        self.label_page_titre = QLabel(self.content_area)
        self.label_page_titre.setObjectName(u"label_page_titre")

        self.topBar.addWidget(self.label_page_titre)

        self.sp_top = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topBar.addItem(self.sp_top)

        self.label_bonjour = QLabel(self.content_area)
        self.label_bonjour.setObjectName(u"label_bonjour")

        self.topBar.addWidget(self.label_bonjour)


        self.contentLayout.addLayout(self.topBar)

        self.stackedWidget = QStackedWidget(self.content_area)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_dashboard = QWidget()
        self.page_dashboard.setObjectName(u"page_dashboard")
        self.dashLayout = QVBoxLayout(self.page_dashboard)
        self.dashLayout.setObjectName(u"dashLayout")
        self.statsRow = QHBoxLayout()
        self.statsRow.setObjectName(u"statsRow")
        self.card_projets = QFrame(self.page_dashboard)
        self.card_projets.setObjectName(u"card_projets")
        self.card_projets.setMinimumSize(QSize(0, 100))
        self.card_projets.setFrameShape(QFrame.StyledPanel)
        self.vboxLayout = QVBoxLayout(self.card_projets)
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.label_nb_projets = QLabel(self.card_projets)
        self.label_nb_projets.setObjectName(u"label_nb_projets")
        self.label_nb_projets.setAlignment(Qt.AlignCenter)

        self.vboxLayout.addWidget(self.label_nb_projets)

        self.label_nb_projets_txt = QLabel(self.card_projets)
        self.label_nb_projets_txt.setObjectName(u"label_nb_projets_txt")
        self.label_nb_projets_txt.setAlignment(Qt.AlignCenter)

        self.vboxLayout.addWidget(self.label_nb_projets_txt)


        self.statsRow.addWidget(self.card_projets)

        self.card_ifc = QFrame(self.page_dashboard)
        self.card_ifc.setObjectName(u"card_ifc")
        self.card_ifc.setMinimumSize(QSize(0, 100))
        self.card_ifc.setFrameShape(QFrame.StyledPanel)
        self.vboxLayout1 = QVBoxLayout(self.card_ifc)
        self.vboxLayout1.setObjectName(u"vboxLayout1")
        self.label_nb_ifc = QLabel(self.card_ifc)
        self.label_nb_ifc.setObjectName(u"label_nb_ifc")
        self.label_nb_ifc.setAlignment(Qt.AlignCenter)

        self.vboxLayout1.addWidget(self.label_nb_ifc)

        self.label_nb_ifc_txt = QLabel(self.card_ifc)
        self.label_nb_ifc_txt.setObjectName(u"label_nb_ifc_txt")
        self.label_nb_ifc_txt.setAlignment(Qt.AlignCenter)

        self.vboxLayout1.addWidget(self.label_nb_ifc_txt)


        self.statsRow.addWidget(self.card_ifc)

        self.card_analyses = QFrame(self.page_dashboard)
        self.card_analyses.setObjectName(u"card_analyses")
        self.card_analyses.setMinimumSize(QSize(0, 100))
        self.card_analyses.setFrameShape(QFrame.StyledPanel)
        self.vboxLayout2 = QVBoxLayout(self.card_analyses)
        self.vboxLayout2.setObjectName(u"vboxLayout2")
        self.label_nb_analyses = QLabel(self.card_analyses)
        self.label_nb_analyses.setObjectName(u"label_nb_analyses")
        self.label_nb_analyses.setAlignment(Qt.AlignCenter)

        self.vboxLayout2.addWidget(self.label_nb_analyses)

        self.label_nb_analyses_txt = QLabel(self.card_analyses)
        self.label_nb_analyses_txt.setObjectName(u"label_nb_analyses_txt")
        self.label_nb_analyses_txt.setAlignment(Qt.AlignCenter)

        self.vboxLayout2.addWidget(self.label_nb_analyses_txt)


        self.statsRow.addWidget(self.card_analyses)


        self.dashLayout.addLayout(self.statsRow)

        self.label_recents_titre = QLabel(self.page_dashboard)
        self.label_recents_titre.setObjectName(u"label_recents_titre")

        self.dashLayout.addWidget(self.label_recents_titre)

        self.table_recents = QTableWidget(self.page_dashboard)
        self.table_recents.setObjectName(u"table_recents")
        self.table_recents.setColumnCount(4)
        self.table_recents.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_recents.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.dashLayout.addWidget(self.table_recents)

        self.stackedWidget.addWidget(self.page_dashboard)
        self.page_projets = QWidget()
        self.page_projets.setObjectName(u"page_projets")
        self.projetsLayout = QVBoxLayout(self.page_projets)
        self.projetsLayout.setObjectName(u"projetsLayout")
        self.table_projets = QTableWidget(self.page_projets)
        self.table_projets.setObjectName(u"table_projets")
        self.table_projets.setColumnCount(4)
        self.table_projets.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_projets.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.projetsLayout.addWidget(self.table_projets)

        self.stackedWidget.addWidget(self.page_projets)
        self.page_nouveau = QWidget()
        self.page_nouveau.setObjectName(u"page_nouveau")
        self.nouveauLayout = QVBoxLayout(self.page_nouveau)
        self.nouveauLayout.setObjectName(u"nouveauLayout")
        self.label_np_titre = QLabel(self.page_nouveau)
        self.label_np_titre.setObjectName(u"label_np_titre")

        self.nouveauLayout.addWidget(self.label_np_titre)

        self.label_np_nom = QLabel(self.page_nouveau)
        self.label_np_nom.setObjectName(u"label_np_nom")

        self.nouveauLayout.addWidget(self.label_np_nom)

        self.input_nom_projet = QLineEdit(self.page_nouveau)
        self.input_nom_projet.setObjectName(u"input_nom_projet")
        self.input_nom_projet.setMinimumSize(QSize(0, 45))

        self.nouveauLayout.addWidget(self.input_nom_projet)

        self.label_np_ifc = QLabel(self.page_nouveau)
        self.label_np_ifc.setObjectName(u"label_np_ifc")

        self.nouveauLayout.addWidget(self.label_np_ifc)

        self.ifcRow = QHBoxLayout()
        self.ifcRow.setObjectName(u"ifcRow")
        self.input_chemin_ifc = QLineEdit(self.page_nouveau)
        self.input_chemin_ifc.setObjectName(u"input_chemin_ifc")
        self.input_chemin_ifc.setMinimumSize(QSize(0, 45))
        self.input_chemin_ifc.setReadOnly(True)

        self.ifcRow.addWidget(self.input_chemin_ifc)

        self.btn_parcourir = QPushButton(self.page_nouveau)
        self.btn_parcourir.setObjectName(u"btn_parcourir")
        self.btn_parcourir.setMinimumSize(QSize(140, 45))

        self.ifcRow.addWidget(self.btn_parcourir)


        self.nouveauLayout.addLayout(self.ifcRow)

        self.label_np_erreur = QLabel(self.page_nouveau)
        self.label_np_erreur.setObjectName(u"label_np_erreur")
        self.label_np_erreur.setAlignment(Qt.AlignCenter)

        self.nouveauLayout.addWidget(self.label_np_erreur)

        self.btn_creer_projet = QPushButton(self.page_nouveau)
        self.btn_creer_projet.setObjectName(u"btn_creer_projet")
        self.btn_creer_projet.setMinimumSize(QSize(0, 50))

        self.nouveauLayout.addWidget(self.btn_creer_projet)

        self.progress_bar = QProgressBar(self.page_nouveau)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.nouveauLayout.addWidget(self.progress_bar)

        self.spacerItem = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.nouveauLayout.addItem(self.spacerItem)

        self.stackedWidget.addWidget(self.page_nouveau)

        self.contentLayout.addWidget(self.stackedWidget)


        self.mainLayout.addWidget(self.content_area)

        DashboardWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(DashboardWindow)

        QMetaObject.connectSlotsByName(DashboardWindow)
    # setupUi

    def retranslateUi(self, DashboardWindow):
        DashboardWindow.setWindowTitle(QCoreApplication.translate("DashboardWindow", u"BATICALC - Tableau de bord", None))
        self.label_logo.setText(QCoreApplication.translate("DashboardWindow", u"BATICALC", None))
        self.label_user_name.setText(QCoreApplication.translate("DashboardWindow", u"Utilisateur", None))
        self.btn_nav_dashboard.setText(QCoreApplication.translate("DashboardWindow", u"  Tableau de bord", None))
        self.btn_nav_projets.setText(QCoreApplication.translate("DashboardWindow", u"  Mes projets", None))
        self.btn_nav_nouveau.setText(QCoreApplication.translate("DashboardWindow", u"  Nouveau projet", None))
        self.btn_deconnexion.setText(QCoreApplication.translate("DashboardWindow", u"  Deconnexion", None))
        self.label_page_titre.setText(QCoreApplication.translate("DashboardWindow", u"Tableau de bord", None))
        self.label_bonjour.setText(QCoreApplication.translate("DashboardWindow", u"Bonjour !", None))
        self.label_nb_projets.setText(QCoreApplication.translate("DashboardWindow", u"0", None))
        self.label_nb_projets_txt.setText(QCoreApplication.translate("DashboardWindow", u"Projets", None))
        self.label_nb_ifc.setText(QCoreApplication.translate("DashboardWindow", u"0", None))
        self.label_nb_ifc_txt.setText(QCoreApplication.translate("DashboardWindow", u"Fichiers IFC", None))
        self.label_nb_analyses.setText(QCoreApplication.translate("DashboardWindow", u"0", None))
        self.label_nb_analyses_txt.setText(QCoreApplication.translate("DashboardWindow", u"Analyses", None))
        self.label_recents_titre.setText(QCoreApplication.translate("DashboardWindow", u"Projets recents", None))
        self.label_np_titre.setText(QCoreApplication.translate("DashboardWindow", u"Nouveau projet", None))
        self.label_np_nom.setText(QCoreApplication.translate("DashboardWindow", u"Nom du projet", None))
        self.input_nom_projet.setPlaceholderText(QCoreApplication.translate("DashboardWindow", u"Ex: Batiment A - Fondations", None))
        self.label_np_ifc.setText(QCoreApplication.translate("DashboardWindow", u"Fichier IFC", None))
        self.input_chemin_ifc.setPlaceholderText(QCoreApplication.translate("DashboardWindow", u"Chemin vers le fichier .ifc", None))
        self.btn_parcourir.setText(QCoreApplication.translate("DashboardWindow", u"Parcourir...", None))
        self.label_np_erreur.setText("")
        self.btn_creer_projet.setText(QCoreApplication.translate("DashboardWindow", u"Creer le projet et analyser", None))
    # retranslateUi

