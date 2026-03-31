# src/ui_handlers/dashboard_handler.py
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                QPushButton, QLabel, QLineEdit, QFileDialog,
                                QTableWidget, QTableWidgetItem, QHeaderView,
                                QStackedWidget, QFrame, QProgressBar,
                                QGraphicsOpacityEffect, QSizePolicy, QSpacerItem)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont
from generated.ui_dashboard import Ui_DashboardWindow
from src.base_de_donnees import get_projets_utilisateur, creer_projet
import session 



SIDEBAR_STYLE = """
QWidget#sidebar {
    background: #0D1117;
    border-right: 1px solid rgba(255,255,255,0.07);
}
QLabel#logo {
    color: #F5C842;
    font-family: 'Georgia';
    font-size: 22px;
    font-weight: bold;
    letter-spacing: 4px;
    padding: 0px 20px;
}
QLabel#logo_sub {
    color: rgba(255,255,255,0.25);
    font-size: 9px;
    letter-spacing: 3px;
    padding: 0px 20px;
}
QLabel#user_name {
    color: rgba(255,255,255,0.8);
    font-size: 13px;
    font-weight: bold;
    padding: 0px 20px;
}
QLabel#user_role {
    color: rgba(255,255,255,0.3);
    font-size: 10px;
    letter-spacing: 1px;
    padding: 0px 20px;
}
QPushButton.nav_btn {
    background: transparent;
    color: rgba(255,255,255,0.45);
    border: none;
    text-align: left;
    padding: 0px 20px;
    min-height: 46px;
    font-size: 13px;
    border-radius: 0px;
}
QPushButton.nav_btn:hover {
    background: rgba(255,255,255,0.05);
    color: rgba(255,255,255,0.85);
}
QPushButton.nav_btn:checked {
    background: rgba(245,200,66,0.1);
    color: #F5C842;
    border-left: 3px solid #F5C842;
}
QPushButton#btn_deconnexion {
    background: transparent;
    color: rgba(255,107,107,0.6);
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    text-align: left;
    padding: 0px 20px;
    min-height: 46px;
    font-size: 13px;
}
QPushButton#btn_deconnexion:hover {
    background: rgba(255,107,107,0.08);
    color: #FF6B6B;
}
"""

CONTENT_STYLE = """
QWidget#content {
    background: #0A0F14;
}
QLabel#page_title {
    color: #FFFFFF;
    font-size: 20px;
    font-weight: bold;
    font-family: 'Georgia';
}
QLabel#greeting {
    color: rgba(255,255,255,0.35);
    font-size: 12px;
    letter-spacing: 1px;
}
QWidget#stat_card {
    background: #13191F;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
}
QLabel#stat_number {
    color: #F5C842;
    font-size: 36px;
    font-weight: bold;
}
QLabel#stat_label {
    color: rgba(255,255,255,0.4);
    font-size: 10px;
    letter-spacing: 2px;
}
QLabel#stat_icon {
    color: rgba(245,200,66,0.25);
    font-size: 28px;
}
QLabel#section_title {
    color: rgba(255,255,255,0.7);
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 2px;
}
QTableWidget {
    background: #13191F;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    gridline-color: rgba(255,255,255,0.05);
    color: rgba(255,255,255,0.8);
    font-size: 13px;
    selection-background-color: rgba(245,200,66,0.12);
    selection-color: #FFFFFF;
    alternate-background-color: rgba(255,255,255,0.02);
}
QTableWidget::item { padding: 10px 14px; border: none; }
QTableWidget::item:selected { background: rgba(245,200,66,0.12); color: #FFFFFF; }
QHeaderView::section {
    background: #0D1117;
    color: rgba(255,255,255,0.35);
    font-weight: bold;
    font-size: 10px;
    letter-spacing: 2px;
    padding: 10px 14px;
    border: none;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
QLabel#form_title {
    color: #FFFFFF;
    font-size: 18px;
    font-weight: bold;
    font-family: 'Georgia';
}
QLabel#form_sub { color: rgba(255,255,255,0.35); font-size: 12px; }
QLabel#field_label {
    color: rgba(255,255,255,0.5);
    font-size: 10px;
    letter-spacing: 2px;
    font-weight: bold;
}
QLineEdit {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    color: #FFFFFF;
    font-size: 13px;
    padding: 12px 16px;
}
QLineEdit:focus {
    border: 1.5px solid #F5C842;
    background: rgba(245,200,66,0.04);
}
QLineEdit:read-only {
    color: rgba(255,255,255,0.4);
}
QPushButton#btn_browse {
    background: rgba(255,255,255,0.05);
    color: rgba(255,255,255,0.6);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    font-size: 13px;
    padding: 12px 20px;
    min-width: 130px;
}
QPushButton#btn_browse:hover {
    background: rgba(255,255,255,0.09);
    color: #FFFFFF;
}
QPushButton#btn_create {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #F5C842, stop:1 #E8A020);
    color: #0D1117;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
    min-height: 52px;
}
QPushButton#btn_create:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #FFD55A, stop:1 #F0B030);
}
QPushButton#btn_create:disabled {
    background: rgba(255,255,255,0.08);
    color: rgba(255,255,255,0.2);
}
QLabel#error_lbl {
    color: #FF6B6B;
    font-size: 12px;
    background: rgba(255,107,107,0.1);
    border: 1px solid rgba(255,107,107,0.25);
    border-radius: 8px;
    padding: 8px 14px;
}
QProgressBar {
    background: rgba(255,255,255,0.06);
    border: none;
    border-radius: 6px;
    height: 8px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #F5C842, stop:1 #E8A020);
    border-radius: 6px;
}
"""


class DashboardWindow(QMainWindow):
    def __init__(self, utilisateur: dict):
        super().__init__()
        self.utilisateur = utilisateur
        self.setWindowTitle("BATICALC — Tableau de bord")
        self.resize(1200, 760)
        self._build_ui()
        self.center()
        self._charger_donnees()

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(self.screen().availableGeometry().center())
        self.move(qr.topLeft())

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ═══════════════════════════════════════
        #  SIDEBAR
        # ═══════════════════════════════════════
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(SIDEBAR_STYLE)
        sv = QVBoxLayout(sidebar)
        sv.setContentsMargins(0, 0, 0, 0)
        sv.setSpacing(0)

        # Logo
        sv.addSpacing(28)
        logo = QLabel("BATICALC")
        logo.setObjectName("logo")
        sv.addWidget(logo)
        logo_sub = QLabel("CALCULATEUR BIM")
        logo_sub.setObjectName("logo_sub")
        sv.addWidget(logo_sub)

        # Divider
        sv.addSpacing(20)
        div1 = QLabel()
        div1.setFixedHeight(1)
        div1.setStyleSheet("background: rgba(255,255,255,0.06); margin: 0px 20px;")
        sv.addWidget(div1)
        sv.addSpacing(20)

        # User info
        self.lbl_user = QLabel("")
        self.lbl_user.setObjectName("user_name")
        sv.addWidget(self.lbl_user)
        role_lbl = QLabel("UTILISATEUR")
        role_lbl.setObjectName("user_role")
        sv.addWidget(role_lbl)

        sv.addSpacing(24)
        div2 = QLabel()
        div2.setFixedHeight(1)
        div2.setStyleSheet("background: rgba(255,255,255,0.06); margin: 0px 20px;")
        sv.addWidget(div2)
        sv.addSpacing(8)

        # Nav buttons
        nav_items = [
            ("btn_nav_dash",   "  Tableau de bord"),
            ("btn_nav_proj",   "  Mes projets"),
            ("btn_nav_new",    "  Nouveau projet"),
        ]
        self.nav_btns = []
        for name, label in nav_items:
            btn = QPushButton(label)
            btn.setProperty("class", "nav_btn")
            btn.setObjectName(name)
            btn.setStyleSheet(SIDEBAR_STYLE)
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            sv.addWidget(btn)
            self.nav_btns.append(btn)

        sv.addStretch()

        self.btn_deconnexion = QPushButton("  Déconnexion")
        self.btn_deconnexion.setObjectName("btn_deconnexion")
        self.btn_deconnexion.setStyleSheet(SIDEBAR_STYLE)
        self.btn_deconnexion.setCursor(Qt.PointingHandCursor)
        sv.addWidget(self.btn_deconnexion)
        sv.addSpacing(16)

        root.addWidget(sidebar)

        # ═══════════════════════════════════════
        #  CONTENT AREA
        # ═══════════════════════════════════════
        content = QWidget()
        content.setObjectName("content")
        content.setStyleSheet(CONTENT_STYLE)
        cv = QVBoxLayout(content)
        cv.setContentsMargins(0, 0, 0, 0)
        cv.setSpacing(0)

        # Top bar
        topbar = QWidget()
        topbar.setStyleSheet("background: #0D1117; border-bottom: 1px solid rgba(255,255,255,0.06);")
        topbar.setFixedHeight(64)
        tb = QHBoxLayout(topbar)
        tb.setContentsMargins(32, 0, 32, 0)
        self.lbl_page_title = QLabel("Tableau de bord")
        self.lbl_page_title.setObjectName("page_title")
        tb.addWidget(self.lbl_page_title)
        tb.addStretch()
        self.lbl_greeting = QLabel("")
        self.lbl_greeting.setObjectName("greeting")
        tb.addWidget(self.lbl_greeting)
        cv.addWidget(topbar)

        # Stacked pages
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: #0A0F14;")
        cv.addWidget(self.stack)

        self._build_page_dashboard()
        self._build_page_projects()
        self._build_page_new()

        root.addWidget(content)

        # Connections
        self.nav_btns[0].clicked.connect(lambda: self._nav(0, "Tableau de bord", 0))
        self.nav_btns[1].clicked.connect(lambda: self._nav(1, "Mes projets", 1))
        self.nav_btns[2].clicked.connect(lambda: self._nav(2, "Nouveau projet", 2))
        self.btn_deconnexion.clicked.connect(self.on_deconnexion)
        self.nav_btns[0].setChecked(True)

    # ─── Page: Dashboard ──────────────────────────────────
    def _build_page_dashboard(self):
        page = QWidget()
        v = QVBoxLayout(page)
        v.setContentsMargins(32, 32, 32, 32)
        v.setSpacing(0)

        # Stats row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(20)
        self.lbl_nb_projets   = self._stat_card(stats_row, "0", "PROJETS",    "◈")
        self.lbl_nb_ifc       = self._stat_card(stats_row, "0", "FICHIERS IFC","◉")
        self.lbl_nb_analyses  = self._stat_card(stats_row, "0", "ANALYSES",   "◆")
        v.addLayout(stats_row)

        v.addSpacing(32)

        sec = QLabel("PROJETS RÉCENTS")
        sec.setObjectName("section_title")
        v.addWidget(sec)
        v.addSpacing(12)

        self.table_recents = self._make_table(["Nom du projet", "Fichier IFC", "Statut", "Date"])
        v.addWidget(self.table_recents)

        self.stack.addWidget(page)

    def _stat_card(self, layout, num, label, icon):
        card = QWidget()
        card.setObjectName("stat_card")
        card.setMinimumHeight(120)
        ch = QHBoxLayout(card)
        ch.setContentsMargins(24, 20, 24, 20)

        left_v = QVBoxLayout()
        left_v.setSpacing(4)
        num_lbl = QLabel(num)
        num_lbl.setObjectName("stat_number")
        lbl_lbl = QLabel(label)
        lbl_lbl.setObjectName("stat_label")
        left_v.addWidget(num_lbl)
        left_v.addWidget(lbl_lbl)
        left_v.addStretch()
        ch.addLayout(left_v)
        ch.addStretch()

        icon_lbl = QLabel(icon)
        icon_lbl.setObjectName("stat_icon")
        ch.addWidget(icon_lbl, alignment=Qt.AlignRight | Qt.AlignVCenter)

        layout.addWidget(card)
        return num_lbl

    # ─── Page: Projects ───────────────────────────────────
    def _build_page_projects(self):
        page = QWidget()
        v = QVBoxLayout(page)
        v.setContentsMargins(32, 32, 32, 32)

        sec = QLabel("TOUS MES PROJETS")
        sec.setObjectName("section_title")
        v.addWidget(sec)
        v.addSpacing(12)

        self.table_projets = self._make_table(["Nom du projet", "Fichier IFC", "Statut", "Date de création"])
        v.addWidget(self.table_projets)

        self.stack.addWidget(page)

    # ─── Page: New Project ────────────────────────────────
    def _build_page_new(self):
        page = QWidget()
        outer = QHBoxLayout(page)
        outer.setContentsMargins(32, 32, 32, 32)

        # Centered form card
        card = QWidget()
        card.setFixedWidth(560)
        card.setStyleSheet("""
            QWidget {
                background: #13191F;
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 20px;
            }
        """)
        fv = QVBoxLayout(card)
        fv.setContentsMargins(40, 40, 40, 40)
        fv.setSpacing(0)

        form_title = QLabel("Nouveau projet")
        form_title.setObjectName("form_title")
        form_title.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: bold; font-family: Georgia; background: transparent; border: none;")
        fv.addWidget(form_title)

        form_sub = QLabel("Importez un fichier IFC pour démarrer l'analyse")
        form_sub.setStyleSheet("color: rgba(255,255,255,0.35); font-size: 12px; background: transparent; border: none;")
        fv.addSpacing(6)
        fv.addWidget(form_sub)

        fv.addSpacing(8)
        sep = QLabel()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background: rgba(255,255,255,0.07); border: none;")
        fv.addWidget(sep)
        fv.addSpacing(28)

        # Nom
        lbl_nom = QLabel("NOM DU PROJET")
        lbl_nom.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 10px; letter-spacing: 2px; font-weight: bold; background: transparent; border: none;")
        fv.addWidget(lbl_nom)
        fv.addSpacing(8)
        self.input_nom_projet = QLineEdit()
        self.input_nom_projet.setPlaceholderText("Ex: Bâtiment A — Fondations")
        self.input_nom_projet.setStyleSheet("""
            QLineEdit {
                background: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 10px;
                color: #FFFFFF;
                font-size: 13px;
                padding: 12px 16px;
            }
            QLineEdit:focus {
                border: 1.5px solid #F5C842;
                background: rgba(245,200,66,0.04);
            }
        """)
        fv.addWidget(self.input_nom_projet)

        fv.addSpacing(22)

        # Fichier IFC
        lbl_ifc = QLabel("FICHIER IFC")
        lbl_ifc.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 10px; letter-spacing: 2px; font-weight: bold; background: transparent; border: none;")
        fv.addWidget(lbl_ifc)
        fv.addSpacing(8)

        ifc_row = QHBoxLayout()
        ifc_row.setSpacing(10)
        self.input_chemin_ifc = QLineEdit()
        self.input_chemin_ifc.setReadOnly(True)
        self.input_chemin_ifc.setPlaceholderText("Sélectionnez un fichier .ifc...")
        self.input_chemin_ifc.setStyleSheet("""
            QLineEdit {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 10px;
                color: rgba(255,255,255,0.45);
                font-size: 13px;
                padding: 12px 16px;
            }
        """)
        self.btn_parcourir = QPushButton("Parcourir")
        self.btn_parcourir.setObjectName("btn_browse")
        self.btn_parcourir.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.05);
                color: rgba(255,255,255,0.6);
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 10px;
                font-size: 13px;
                padding: 12px 20px;
                min-width: 110px;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.09);
                color: #FFFFFF;
            }
        """)
        self.btn_parcourir.setCursor(Qt.PointingHandCursor)
        ifc_row.addWidget(self.input_chemin_ifc)
        ifc_row.addWidget(self.btn_parcourir)
        fv.addLayout(ifc_row)

        fv.addSpacing(14)

        self.lbl_np_erreur = QLabel("")
        self.lbl_np_erreur.setStyleSheet("color: #FF6B6B; font-size: 12px; background: rgba(255,107,107,0.1); border: 1px solid rgba(255,107,107,0.25); border-radius: 8px; padding: 8px 14px;")
        self.lbl_np_erreur.hide()
        fv.addWidget(self.lbl_np_erreur)

        fv.addSpacing(28)

        self.btn_creer_projet = QPushButton("Analyser le fichier IFC →")
        self.btn_creer_projet.setObjectName("btn_create")
        self.btn_creer_projet.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #F5C842, stop:1 #E8A020);
                color: #0D1117;
                border: none;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                min-height: 52px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #FFD55A, stop:1 #F0B030);
            }
            QPushButton:disabled {
                background: rgba(255,255,255,0.08);
                color: rgba(255,255,255,0.2);
            }
        """)
        self.btn_creer_projet.setCursor(Qt.PointingHandCursor)
        fv.addWidget(self.btn_creer_projet)

        fv.addSpacing(16)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: rgba(255,255,255,0.06);
                border: none;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #F5C842, stop:1 #E8A020);
                border-radius: 3px;
            }
        """)
        fv.addWidget(self.progress_bar)
        fv.addStretch()

        outer.addStretch()
        outer.addWidget(card, alignment=Qt.AlignVCenter)
        outer.addStretch()

        self.stack.addWidget(page)

        self.btn_parcourir.clicked.connect(self.on_parcourir)
        self.btn_creer_projet.clicked.connect(self.on_creer_projet)

    def _make_table(self, headers):
        t = QTableWidget()
        t.setColumnCount(len(headers))
        t.setHorizontalHeaderLabels(headers)
        t.setEditTriggers(QTableWidget.NoEditTriggers)
        t.setSelectionBehavior(QTableWidget.SelectRows)
        t.setAlternatingRowColors(True)
        t.verticalHeader().setVisible(False)
        t.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, len(headers)):
            t.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        t.setShowGrid(False)
        return t

    def _nav(self, btn_idx, title, page_idx):
        for i, b in enumerate(self.nav_btns):
            b.setChecked(i == btn_idx)
        self.lbl_page_title.setText(title)
        self.stack.setCurrentIndex(page_idx)
        if page_idx == 1:
            self._actualiser_projets()

    def _charger_donnees(self):
        nom = self.utilisateur.get("nom", "Utilisateur")
        self.lbl_user.setText(nom)
        self.lbl_greeting.setText(f"Bonjour, {nom}  ✦")
        self._actualiser_projets()

    def _actualiser_projets(self):
        projets = get_projets_utilisateur(self.utilisateur["id"])
        self.lbl_nb_projets.setText(str(len(projets)))
        self.lbl_nb_ifc.setText(str(sum(1 for p in projets if p.get("chemin_ifc"))))
        self.lbl_nb_analyses.setText(str(sum(1 for p in projets if p.get("statut") == "termine")))

        for table in [self.table_recents, self.table_projets]:
            table.setRowCount(0)
            for p in projets:
                row = table.rowCount()
                table.insertRow(row)
                table.setItem(row, 0, QTableWidgetItem(p.get("nom", "")))
                ifc = p.get("chemin_ifc") or "—"
                table.setItem(row, 1, QTableWidgetItem(ifc.split("\\")[-1].split("/")[-1]))
                statut = p.get("statut", "")
                statut_item = QTableWidgetItem(statut)
                if statut == "termine":
                    statut_item.setForeground(QColor("#2ECC71"))
                elif statut == "en_cours":
                    statut_item.setForeground(QColor("#F5C842"))
                else:
                    statut_item.setForeground(QColor("#888888"))
                table.setItem(row, 2, statut_item)
                table.setItem(row, 3, QTableWidgetItem(str(p.get("cree_le", ""))[:10]))

    def on_parcourir(self):
        chemin, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner un fichier IFC", "", "Fichiers IFC (*.ifc);;Tous (*)")
        if chemin:
            self.input_chemin_ifc.setText(chemin)

    def on_creer_projet(self):
        nom = self.ui.input_nom_projet.text().strip()
        chemin = self.ui.input_chemin_ifc.text().strip()
        
        if not nom or not chemin:
            msg = "Veuillez saisir un nom." if not nom else "Veuillez sélectionner un fichier IFC."
            self.ui.label_np_erreur.setText(msg)
            return

        self.ui.label_np_erreur.setText("")
        self.ui.progress_bar.setValue(40)
        self.ui.btn_creer_projet.setEnabled(False)

        # Appel de la logique métier
        res = creer_projet(self.utilisateur["id"], nom, chemin)

        if res["succes"]:
            # Mise à jour de la session globale
            session.projet_actuel.update({
                "id": res["projet_id"],
                "nom": nom,
                "chemin": chemin,
                "actif": True
            })

            # Nettoyage
            self.ui.input_nom_projet.clear()
            self.ui.input_chemin_ifc.clear()
            self.ui.progress_bar.setValue(0)
            self.ui.btn_creer_projet.setEnabled(True)

            # Transition
            from src.ui_handlers.results_handler import ResultsWindow
            self.results = ResultsWindow(
                chemin_ifc=chemin, nom_projet=nom,
                utilisateur=self.utilisateur, dashboard_ref=self
            )
            self.results.show()
            self.hide()
        else:
            # En cas d'échec
            self.ui.label_np_erreur.setText(f"Erreur : {res['erreur']}")
            self.ui.btn_creer_projet.setEnabled(True)
            self.ui.progress_bar.setValue(0) # Reset car l'opération a échoué

    def on_deconnexion(self):
        from src.ui_handlers.welcome_handler import WelcomeWindow
        self.welcome = WelcomeWindow()
        self.welcome.show()
        self.close()
