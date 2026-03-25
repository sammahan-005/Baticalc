# src/ui_handlers/dashboard_handler.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QFileDialog,
                                QTableWidgetItem, QHeaderView)
from generated.ui_dashboard import Ui_DashboardWindow
from src.authentification import get_projets_utilisateur, creer_projet

SIDEBAR = """
    QWidget#sidebar { background-color: #2c3e50; }
    QLabel#label_logo { color: #3498db; font-size: 20px; font-weight: bold;
        border-bottom: 1px solid #34495e; padding-bottom: 10px; }
    QLabel#label_user_name { color: #bdc3c7; font-size: 12px; padding: 5px; }
    QPushButton#btn_nav_dashboard,
    QPushButton#btn_nav_projets,
    QPushButton#btn_nav_nouveau {
        background-color: transparent; color: #bdc3c7; border: none;
        text-align: left; padding-left: 25px; font-size: 14px;
    }
    QPushButton#btn_nav_dashboard:hover,
    QPushButton#btn_nav_projets:hover,
    QPushButton#btn_nav_nouveau:hover { background-color: #34495e; color: white; }
    QPushButton#btn_nav_dashboard:checked,
    QPushButton#btn_nav_projets:checked,
    QPushButton#btn_nav_nouveau:checked { background-color: #3498db; color: white; }
    QPushButton#btn_deconnexion {
        background-color: transparent; color: #e74c3c; border: none;
        text-align: left; padding-left: 25px; font-size: 14px;
        border-top: 1px solid #34495e;
    }
    QPushButton#btn_deconnexion:hover { background-color: #c0392b; color: white; }
"""
CONTENT = """
    QWidget#content_area { background-color: #f0f3f7; }
    QLabel#label_page_titre { color: #2c3e50; font-size: 22px; font-weight: bold; }
    QLabel#label_bonjour    { color: #7f8c8d; font-size: 13px; }
    QLabel#label_recents_titre, QLabel#label_np_titre {
        color: #2c3e50; font-size: 16px; font-weight: bold; }
    QLabel#label_np_nom, QLabel#label_np_ifc {
        color: #34495e; font-size: 13px; font-weight: bold; }
    QLabel#label_np_erreur { color: #e74c3c; font-size: 13px; }
    QFrame#card_projets, QFrame#card_ifc, QFrame#card_analyses {
        background-color: white; border-radius: 8px; border: none; }
    QLabel#label_nb_projets, QLabel#label_nb_ifc, QLabel#label_nb_analyses {
        color: #3498db; font-size: 32px; font-weight: bold; }
    QLabel#label_nb_projets_txt, QLabel#label_nb_ifc_txt,
    QLabel#label_nb_analyses_txt { color: #7f8c8d; font-size: 13px; }
    QTableWidget { background-color: white; border: none; border-radius: 8px;
        gridline-color: #ecf0f1; font-size: 13px; }
    QTableWidget::item { padding: 8px; color: #2c3e50; }
    QTableWidget::item:selected { background-color: #d6eaf8; color: #2c3e50; }
    QHeaderView::section { background-color: #f8f9fa; color: #7f8c8d;
        font-weight: bold; font-size: 12px; padding: 8px; border: none;
        border-bottom: 2px solid #ecf0f1; }
    QLineEdit { border: 2px solid #bdc3c7; border-radius: 5px;
        padding: 8px 12px; font-size: 14px;
        background-color: white; color: #2c3e50; }
    QLineEdit:focus { border: 2px solid #3498db; }
    QPushButton#btn_parcourir {
        background-color: #ecf0f1; color: #2c3e50;
        border: 2px solid #bdc3c7; border-radius: 5px; font-size: 14px; }
    QPushButton#btn_parcourir:hover { background-color: #d5d8dc; }
    QPushButton#btn_creer_projet {
        background-color: #3498db; color: white; border: none;
        border-radius: 5px; font-size: 15px; font-weight: bold; }
    QPushButton#btn_creer_projet:hover { background-color: #2980b9; }
    QProgressBar { border: 2px solid #bdc3c7; border-radius: 5px;
        background-color: white; text-align: center; color: #2c3e50; }
    QProgressBar::chunk { background-color: #3498db; border-radius: 3px; }
"""


class DashboardWindow(QMainWindow):
    def __init__(self, utilisateur: dict):
        super().__init__()
        self.utilisateur = utilisateur
        self.ui = Ui_DashboardWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("BATICALC - Tableau de bord")
        self.resize(1100, 720)
        self.center()
        self.centralWidget().setStyleSheet("background-color: #f0f3f7;")
        self.ui.sidebar.setStyleSheet(SIDEBAR)
        self.ui.content_area.setStyleSheet(CONTENT)
        self._setup_tables()
        self._setup_connections()
        self._charger_donnees()

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(self.screen().availableGeometry().center())
        self.move(qr.topLeft())

    def _setup_tables(self):
        cols = ["Nom", "Fichier IFC", "Statut", "Date"]
        for table in [self.ui.table_recents, self.ui.table_projets]:
            table.setHorizontalHeaderLabels(cols)
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
            table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
            table.verticalHeader().setVisible(False)
            table.setAlternatingRowColors(True)

    def _setup_connections(self):
        self.ui.btn_nav_dashboard.clicked.connect(
            lambda: self._naviguer(0, "Tableau de bord", self.ui.btn_nav_dashboard))
        self.ui.btn_nav_projets.clicked.connect(
            lambda: self._naviguer(1, "Mes projets", self.ui.btn_nav_projets))
        self.ui.btn_nav_nouveau.clicked.connect(
            lambda: self._naviguer(2, "Nouveau projet", self.ui.btn_nav_nouveau))
        self.ui.btn_deconnexion.clicked.connect(self.on_deconnexion)
        self.ui.btn_parcourir.clicked.connect(self.on_parcourir)
        self.ui.btn_creer_projet.clicked.connect(self.on_creer_projet)

    def _charger_donnees(self):
        nom = self.utilisateur.get("nom", "Utilisateur")
        self.ui.label_user_name.setText(nom)
        self.ui.label_bonjour.setText(f"Bonjour, {nom} !")
        self._actualiser_projets()

    def _naviguer(self, index, titre, btn_actif):
        for b in [self.ui.btn_nav_dashboard,
                  self.ui.btn_nav_projets,
                  self.ui.btn_nav_nouveau]:
            b.setChecked(False)
        btn_actif.setChecked(True)
        self.ui.stackedWidget.setCurrentIndex(index)
        self.ui.label_page_titre.setText(titre)
        if index == 1:
            self._actualiser_projets()

    def _actualiser_projets(self):
        projets = get_projets_utilisateur(self.utilisateur["id"])
        self.ui.label_nb_projets.setText(str(len(projets)))
        self.ui.label_nb_ifc.setText(str(sum(1 for p in projets if p.get("chemin_ifc"))))
        self.ui.label_nb_analyses.setText(str(len(projets)))
        for table in [self.ui.table_recents, self.ui.table_projets]:
            table.setRowCount(0)
            for p in projets:
                row = table.rowCount()
                table.insertRow(row)
                table.setItem(row, 0, QTableWidgetItem(p.get("nom", "")))
                ifc = p.get("chemin_ifc") or "—"
                table.setItem(row, 1, QTableWidgetItem(ifc.split("\\")[-1].split("/")[-1]))
                table.setItem(row, 2, QTableWidgetItem(p.get("statut", "")))
                table.setItem(row, 3, QTableWidgetItem(p.get("cree_le", "")[:10]))

    def on_parcourir(self):
        chemin, _ = QFileDialog.getOpenFileName(
            self, "Selectionner un fichier IFC",
            "", "Fichiers IFC (*.ifc);;Tous les fichiers (*)")
        if chemin:
            self.ui.input_chemin_ifc.setText(chemin)

    def on_creer_projet(self):
        nom   = self.ui.input_nom_projet.text().strip()
        chemin = self.ui.input_chemin_ifc.text().strip()
        if not nom:
            self.ui.label_np_erreur.setText("Veuillez saisir un nom de projet.")
            return
        if not chemin:
            self.ui.label_np_erreur.setText("Veuillez selectionner un fichier IFC.")
            return

        self.ui.label_np_erreur.setText("")
        self.ui.progress_bar.setValue(40)
        self.ui.btn_creer_projet.setEnabled(False)

        res = creer_projet(self.utilisateur["id"], nom, chemin)
        self.ui.progress_bar.setValue(100)
        self.ui.btn_creer_projet.setEnabled(True)

        if res["succes"]:
            self.ui.input_nom_projet.clear()
            self.ui.input_chemin_ifc.clear()
            self.ui.progress_bar.setValue(0)
            from src.ui_handlers.results_handler import ResultsWindow
            self.results = ResultsWindow(
                chemin_ifc=chemin,
                nom_projet=nom,
                utilisateur=self.utilisateur,
                dashboard_ref=self
            )
            self.results.show()
            self.hide()
        else:
            self.ui.label_np_erreur.setText(res["erreur"])

    def on_deconnexion(self):
        from src.ui_handlers.welcome_handler import WelcomeWindow
        self.welcome = WelcomeWindow()
        self.welcome.show()
        self.close()