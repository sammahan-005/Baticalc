# src/ui_handlers/dashboard_handler.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import session
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QFileDialog, QFrame,
    QStackedWidget, QProgressBar, QSizePolicy
)
from PySide6.QtGui import QFont
from src.base_de_donnees import get_projets_utilisateur, creer_projet

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY      = "#0D1117"
NAVY2     = "#13191F"
NAVY3     = "#1A2332"
AMBER     = "#F5C842"
AMBER2    = "#E8A020"
WHITE     = "#FFFFFF"
GREY1     = "#8892A4"
GREY2     = "rgba(255,255,255,0.06)"
DANGER    = "#E53E3E"
SUCCESS   = "#38A169"

STYLE = f"""
QMainWindow, QWidget {{
    background: {NAVY};
    font-family: 'Segoe UI', sans-serif;
}}

/* ── SIDEBAR ──────────────────────────────── */
QWidget#sidebar {{
    background: {NAVY2};
    border-right: 1px solid rgba(255,255,255,0.07);
}}
QLabel#lbl_logo {{
    color: {AMBER};
    font-size: 17px;
    font-weight: 900;
    letter-spacing: 3px;
}}
QWidget#user_card {{
    background: {NAVY3};
    border-bottom: 1px solid rgba(255,255,255,0.06);
}}
QLabel#lbl_avatar {{
    background: {AMBER};
    color: {NAVY};
    border-radius: 20px;
    font-size: 13px;
    font-weight: bold;
}}
QLabel#lbl_username {{
    color: {WHITE};
    font-size: 13px;
    font-weight: bold;
}}
QLabel#lbl_role {{
    color: {GREY1};
    font-size: 11px;
}}
QLabel#lbl_nav_section, QLabel#lbl_acct_section {{
    color: rgba(255,255,255,0.25);
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 2px;
    padding-left: 24px;
}}
QPushButton#nav_btn {{
    background: transparent;
    color: {GREY1};
    border: none;
    border-left: 3px solid transparent;
    text-align: left;
    padding-left: 21px;
    font-size: 13px;
    font-weight: 500;
    min-height: 52px;
}}
QPushButton#nav_btn:hover {{
    background: rgba(255,255,255,0.04);
    color: {WHITE};
}}
QPushButton#nav_btn:checked {{
    background: rgba(245,200,66,0.08);
    color: {AMBER};
    border-left: 3px solid {AMBER};
    font-weight: bold;
}}
QPushButton#btn_logout {{
    background: transparent;
    color: {DANGER};
    border: none;
    border-top: 1px solid rgba(255,255,255,0.07);
    text-align: left;
    padding-left: 24px;
    font-size: 13px;
    min-height: 52px;
}}
QPushButton#btn_logout:hover {{
    background: rgba(229,62,62,0.08);
}}

/* ── TOP BAR ──────────────────────────────── */
QWidget#topbar {{
    background: {NAVY2};
    border-bottom: 1px solid rgba(255,255,255,0.07);
}}
QLabel#lbl_page_title {{
    color: {WHITE};
    font-size: 20px;
    font-weight: bold;
}}
QLabel#lbl_greeting {{
    color: {GREY1};
    font-size: 13px;
}}

/* ── STAT CARDS ───────────────────────────── */
QFrame#stat_card {{
    background: {NAVY2};
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
}}
QLabel#stat_num {{
    color: {AMBER};
    font-size: 36px;
    font-weight: 900;
}}
QLabel#stat_lbl {{
    color: {GREY1};
    font-size: 11px;
    letter-spacing: 1px;
}}

/* ── SECTION TITLES ───────────────────────── */
QLabel#section_title {{
    color: {WHITE};
    font-size: 15px;
    font-weight: bold;
}}

/* ── TABLES ───────────────────────────────── */
QTableWidget {{
    background: {NAVY2};
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    gridline-color: rgba(255,255,255,0.04);
    color: rgba(255,255,255,0.8);
    font-size: 13px;
    alternate-background-color: rgba(255,255,255,0.02);
    selection-background-color: rgba(245,200,66,0.1);
    outline: none;
}}
QTableWidget::item {{ padding: 12px 16px; border: none; }}
QTableWidget::item:selected {{ background: rgba(245,200,66,0.12); color: {WHITE}; }}
QHeaderView::section {{
    background: {NAVY};
    color: rgba(255,255,255,0.3);
    font-weight: bold;
    font-size: 10px;
    letter-spacing: 2px;
    padding: 10px 16px;
    border: none;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}}

/* ── NEW PROJECT CARD ─────────────────────── */
QFrame#project_card {{
    background: {NAVY2};
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
}}
QLabel#form_label {{
    color: rgba(255,255,255,0.4);
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 2px;
}}
QLabel#form_error {{
    color: {DANGER};
    font-size: 12px;
}}
QLineEdit {{
    background: rgba(255,255,255,0.05);
    color: {WHITE};
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 0 16px;
    font-size: 14px;
    min-height: 50px;
    selection-background-color: {AMBER};
    selection-color: {NAVY};
}}
QLineEdit:focus {{
    border: 1px solid {AMBER};
    background: rgba(245,200,66,0.05);
}}
QLineEdit[readOnly="true"] {{
    color: {GREY1};
}}
QPushButton#btn_browse {{
    background: rgba(255,255,255,0.05);
    color: rgba(255,255,255,0.6);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    min-height: 50px;
    min-width: 130px;
    padding: 0 16px;
}}
QPushButton#btn_browse:hover {{
    border-color: {AMBER};
    color: {AMBER};
    background: rgba(245,200,66,0.05);
}}
QPushButton#btn_launch {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {AMBER}, stop:1 {AMBER2});
    color: {NAVY};
    border: none;
    border-radius: 10px;
    font-size: 15px;
    font-weight: bold;
    min-height: 54px;
}}
QPushButton#btn_launch:hover {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #FFD55A, stop:1 #F0B030);
}}
QPushButton#btn_launch:disabled {{
    background: rgba(255,255,255,0.07);
    color: rgba(255,255,255,0.25);
}}
QProgressBar {{
    background: rgba(255,255,255,0.07);
    border: none;
    border-radius: 4px;
    max-height: 6px;
    text-align: center;
}}
QProgressBar::chunk {{
    background: {AMBER};
    border-radius: 4px;
}}
"""


class DashboardWindow(QMainWindow):
    def __init__(self, utilisateur: dict):
        super().__init__()
        self.utilisateur = utilisateur
        self.setWindowTitle("BATICALC — Tableau de bord")
        self.resize(1200, 760)
        self.setStyleSheet(STYLE)
        self._build_ui()
        self.center()
        self._charger_donnees()

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(self.screen().availableGeometry().center())
        self.move(qr.topLeft())

    # ── Build UI ─────────────────────────────────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_sidebar())
        root.addWidget(self._build_content(), 1)

    def _build_sidebar(self):
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)
        v = QVBoxLayout(sidebar)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        # Logo
        logo_zone = QWidget()
        logo_zone.setFixedHeight(72)
        lz = QHBoxLayout(logo_zone)
        lz.setContentsMargins(24, 0, 24, 0)
        lbl_logo = QLabel("BATICALC")
        lbl_logo.setObjectName("lbl_logo")
        lz.addWidget(lbl_logo)
        v.addWidget(logo_zone)

        # User card
        self.user_card = QWidget()
        self.user_card.setObjectName("user_card")
        self.user_card.setFixedHeight(72)
        uc = QHBoxLayout(self.user_card)
        uc.setContentsMargins(20, 0, 20, 0)
        uc.setSpacing(12)
        self.lbl_avatar = QLabel("U")
        self.lbl_avatar.setObjectName("lbl_avatar")
        self.lbl_avatar.setFixedSize(40, 40)
        self.lbl_avatar.setAlignment(Qt.AlignCenter)
        uc.addWidget(self.lbl_avatar)
        name_col = QVBoxLayout()
        name_col.setSpacing(2)
        self.lbl_username = QLabel("Utilisateur")
        self.lbl_username.setObjectName("lbl_username")
        self.lbl_role = QLabel("Ingenieur BIM")
        self.lbl_role.setObjectName("lbl_role")
        name_col.addWidget(self.lbl_username)
        name_col.addWidget(self.lbl_role)
        uc.addLayout(name_col)
        v.addWidget(self.user_card)

        # Nav label
        lbl_nav = QLabel("NAVIGATION")
        lbl_nav.setObjectName("lbl_nav_section")
        lbl_nav.setFixedHeight(36)
        v.addWidget(lbl_nav)

        # Nav buttons
        self.btn_nav_dash    = self._nav_btn("  Tableau de bord", checked=True)
        self.btn_nav_projets = self._nav_btn("  Mes projets")
        self.btn_nav_nouveau = self._nav_btn("  + Nouveau projet")
        v.addWidget(self.btn_nav_dash)
        v.addWidget(self.btn_nav_projets)
        v.addWidget(self.btn_nav_nouveau)

        v.addStretch()

        # Account label + logout
        lbl_acct = QLabel("COMPTE")
        lbl_acct.setObjectName("lbl_acct_section")
        lbl_acct.setFixedHeight(36)
        v.addWidget(lbl_acct)
        self.btn_logout = QPushButton("  Deconnexion")
        self.btn_logout.setObjectName("btn_logout")
        self.btn_logout.setCursor(Qt.PointingHandCursor)
        v.addWidget(self.btn_logout)
        v.addSpacing(8)

        # Connect nav
        self.btn_nav_dash.clicked.connect(
            lambda: self._naviguer(0, "Tableau de bord", self.btn_nav_dash))
        self.btn_nav_projets.clicked.connect(
            lambda: self._naviguer(1, "Mes projets", self.btn_nav_projets))
        self.btn_nav_nouveau.clicked.connect(
            lambda: self._naviguer(2, "Nouveau projet", self.btn_nav_nouveau))
        self.btn_logout.clicked.connect(self.on_deconnexion)

        return sidebar

    def _nav_btn(self, text, checked=False):
        btn = QPushButton(text)
        btn.setObjectName("nav_btn")
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setCursor(Qt.PointingHandCursor)
        return btn

    def _build_content(self):
        content = QWidget()
        v = QVBoxLayout(content)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        # Top bar
        topbar = QWidget()
        topbar.setObjectName("topbar")
        topbar.setFixedHeight(72)
        tb = QHBoxLayout(topbar)
        tb.setContentsMargins(32, 0, 32, 0)
        self.lbl_page_title = QLabel("Tableau de bord")
        self.lbl_page_title.setObjectName("lbl_page_title")
        self.lbl_greeting = QLabel("Bonjour !")
        self.lbl_greeting.setObjectName("lbl_greeting")
        tb.addWidget(self.lbl_page_title)
        tb.addStretch()
        tb.addWidget(self.lbl_greeting)
        v.addWidget(topbar)

        # Stacked widget
        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_page_dashboard())
        self.stack.addWidget(self._build_page_projets())
        self.stack.addWidget(self._build_page_nouveau())
        v.addWidget(self.stack)

        return content

    # ── Pages ─────────────────────────────────────────────────────────────────

    def _build_page_dashboard(self):
        page = QWidget()
        v = QVBoxLayout(page)
        v.setContentsMargins(32, 28, 32, 32)
        v.setSpacing(24)

        # Stat cards row
        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)
        self.stat_projets  = self._stat_card(cards_row, "0", "PROJETS TOTAL")
        self.stat_ifc      = self._stat_card(cards_row, "0", "FICHIERS IFC")
        self.stat_analyses = self._stat_card(cards_row, "0", "ANALYSES")
        v.addLayout(cards_row)

        # Recent projects title
        lbl = QLabel("Projets recents")
        lbl.setObjectName("section_title")
        v.addWidget(lbl)

        # Recent table
        self.table_recents = self._make_table(["Nom du projet", "Fichier IFC", "Statut", "Date"])
        v.addWidget(self.table_recents)

        return page

    def _build_page_projets(self):
        page = QWidget()
        v = QVBoxLayout(page)
        v.setContentsMargins(32, 28, 32, 32)
        v.setSpacing(16)
        lbl = QLabel("Tous mes projets")
        lbl.setObjectName("section_title")
        v.addWidget(lbl)
        self.table_projets = self._make_table(["Nom du projet", "Fichier IFC", "Statut", "Date"])
        v.addWidget(self.table_projets)
        return page

    def _build_page_nouveau(self):
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(32, 28, 32, 32)
        outer.setSpacing(0)

        card = QFrame()
        card.setObjectName("project_card")
        card.setMaximumWidth(660)
        cv = QVBoxLayout(card)
        cv.setContentsMargins(40, 36, 40, 36)
        cv.setSpacing(0)

        # Title
        lbl_title = QLabel("Nouveau projet d'analyse")
        lbl_title.setObjectName("section_title")
        cv.addWidget(lbl_title)
        cv.addSpacing(4)
        lbl_sub = QLabel("Importez un fichier IFC pour demarrer l'analyse automatique.")
        lbl_sub.setStyleSheet(f"color: {GREY1}; font-size: 13px;")
        lbl_sub.setWordWrap(True)
        cv.addWidget(lbl_sub)
        cv.addSpacing(28)

        # Project name
        lbl_nom = QLabel("NOM DU PROJET")
        lbl_nom.setObjectName("form_label")
        cv.addWidget(lbl_nom)
        cv.addSpacing(8)
        self.input_nom_projet = QLineEdit()
        self.input_nom_projet.setPlaceholderText("Ex: Batiment A — Fondations RDC")
        self.input_nom_projet.setFocusPolicy(Qt.StrongFocus)
        cv.addWidget(self.input_nom_projet)
        cv.addSpacing(20)

        # IFC path
        lbl_ifc = QLabel("FICHIER IFC")
        lbl_ifc.setObjectName("form_label")
        cv.addWidget(lbl_ifc)
        cv.addSpacing(8)
        ifc_row = QHBoxLayout()
        ifc_row.setSpacing(12)
        self.input_chemin_ifc = QLineEdit()
        self.input_chemin_ifc.setPlaceholderText("Aucun fichier selectionne...")
        self.input_chemin_ifc.setReadOnly(True)
        self.input_chemin_ifc.setFocusPolicy(Qt.StrongFocus)
        self.btn_parcourir = QPushButton("Parcourir")
        self.btn_parcourir.setObjectName("btn_browse")
        self.btn_parcourir.setCursor(Qt.PointingHandCursor)
        ifc_row.addWidget(self.input_chemin_ifc)
        ifc_row.addWidget(self.btn_parcourir)
        cv.addLayout(ifc_row)
        cv.addSpacing(10)

        # Error label
        self.lbl_erreur = QLabel("")
        self.lbl_erreur.setObjectName("form_error")
        self.lbl_erreur.setWordWrap(True)
        cv.addWidget(self.lbl_erreur)
        cv.addSpacing(24)

        # Launch button
        self.btn_creer_projet = QPushButton("Lancer l'analyse  →")
        self.btn_creer_projet.setObjectName("btn_launch")
        self.btn_creer_projet.setCursor(Qt.PointingHandCursor)
        cv.addWidget(self.btn_creer_projet)
        cv.addSpacing(16)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        cv.addWidget(self.progress_bar)

        outer.addWidget(card)
        outer.addStretch()

        # Connections
        self.btn_parcourir.clicked.connect(self.on_parcourir)
        self.btn_creer_projet.clicked.connect(self.on_creer_projet)

        return page

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _stat_card(self, layout, num, label):
        card = QFrame()
        card.setObjectName("stat_card")
        card.setMinimumHeight(110)
        cv = QVBoxLayout(card)
        cv.setContentsMargins(24, 20, 24, 20)
        cv.setSpacing(4)
        num_lbl = QLabel(num)
        num_lbl.setObjectName("stat_num")
        lbl_lbl = QLabel(label)
        lbl_lbl.setObjectName("stat_lbl")
        cv.addWidget(num_lbl)
        cv.addWidget(lbl_lbl)
        layout.addWidget(card)
        return num_lbl   # return the label so we can update it

    def _make_table(self, headers):
        t = QTableWidget()
        t.setColumnCount(len(headers))
        t.setHorizontalHeaderLabels(headers)
        t.setEditTriggers(QTableWidget.NoEditTriggers)
        t.setSelectionBehavior(QTableWidget.SelectRows)
        t.setAlternatingRowColors(True)
        t.verticalHeader().setVisible(False)
        t.setShowGrid(False)
        t.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        t.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        for i in range(2, len(headers)):
            t.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        return t

    # ── Data loading ──────────────────────────────────────────────────────────

    def _charger_donnees(self):
        nom = self.utilisateur.get("nom", "Utilisateur")
        initiales = "".join(p[0].upper() for p in nom.split()[:2]) or "U"
        self.lbl_avatar.setText(initiales)
        self.lbl_username.setText(nom)
        self.lbl_greeting.setText(f"Bonjour, {nom.split()[0]} !")
        self._actualiser_projets()

    def _naviguer(self, index, titre, btn_actif):
        for b in [self.btn_nav_dash, self.btn_nav_projets, self.btn_nav_nouveau]:
            b.setChecked(False)
        btn_actif.setChecked(True)
        self.stack.setCurrentIndex(index)
        self.lbl_page_title.setText(titre)
        if index == 1:
            self._actualiser_projets()

    def _actualiser_projets(self):
        projets = get_projets_utilisateur(self.utilisateur["id"])
        self.stat_projets.setText(str(len(projets)))
        self.stat_ifc.setText(str(sum(1 for p in projets if p.get("chemin_ifc"))))
        self.stat_analyses.setText(str(sum(1 for p in projets if p.get("statut") == "termine")))

        for table in [self.table_recents, self.table_projets]:
            table.setRowCount(0)
            for p in projets:
                row = table.rowCount()
                table.insertRow(row)
                table.setRowHeight(row, 48)
                table.setItem(row, 0, QTableWidgetItem(p.get("nom", "")))
                ifc = p.get("chemin_ifc") or "—"
                table.setItem(row, 1, QTableWidgetItem(
                    ifc.split("\\")[-1].split("/")[-1]))
                statut = p.get("statut", "en_attente").replace("_", " ").capitalize()
                table.setItem(row, 2, QTableWidgetItem(statut))
                table.setItem(row, 3, QTableWidgetItem(
                    p.get("cree_le", "")[:10]))

    # ── Actions ───────────────────────────────────────────────────────────────

    def on_parcourir(self):
        chemin, _ = QFileDialog.getOpenFileName(
            self, "Selectionner un fichier IFC",
            "", "Fichiers IFC (*.ifc);;Tous les fichiers (*)")
        if chemin:
            self.input_chemin_ifc.setText(chemin)

    def on_creer_projet(self):
        nom    = self.input_nom_projet.text().strip()
        chemin = self.input_chemin_ifc.text().strip()

        if not nom:
            self.lbl_erreur.setText("Veuillez saisir un nom de projet.")
            return
        if not chemin:
            self.lbl_erreur.setText("Veuillez selectionner un fichier IFC.")
            return

        self.lbl_erreur.setText("")
        self.progress_bar.setValue(40)
        self.btn_creer_projet.setEnabled(False)

        res = creer_projet(self.utilisateur["id"], nom, chemin)
        self.progress_bar.setValue(100)
        self.btn_creer_projet.setEnabled(True)

        if res["succes"]:
            # Update session so parseurIfc knows the current project id
            session.projet_actuel["id"]     = res["projet_id"]
            session.projet_actuel["nom"]    = nom
            session.projet_actuel["chemin"] = chemin
            session.projet_actuel["actif"]  = True

            self.input_nom_projet.clear()
            self.input_chemin_ifc.clear()
            self.progress_bar.setValue(0)

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
            self.lbl_erreur.setText(res["erreur"])

    def on_deconnexion(self):
        from src.ui_handlers.welcome_handler import WelcomeWindow
        self.welcome = WelcomeWindow()
        self.welcome.show()
        self.close()
