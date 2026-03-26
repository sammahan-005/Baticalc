# src/ui_handlers/results_handler.py
import os
from PySide6.QtCore import Qt, QThread, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                                QHeaderView, QTabWidget, QTextEdit, QMessageBox,
                                QFileDialog, QGraphicsOpacityEffect, QFrame)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen

STYLE = """
QMainWindow, QWidget {
    background: #0A0F14;
}
/* ── Top bar ─────────────────────────────────── */
QWidget#topbar {
    background: #0D1117;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
QLabel#app_brand {
    color: #F5C842;
    font-family: 'Georgia';
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 3px;
}
QLabel#result_title {
    color: #FFFFFF;
    font-size: 18px;
    font-weight: bold;
    font-family: 'Georgia';
}
QLabel#project_name {
    color: rgba(245,200,66,0.7);
    font-size: 12px;
    letter-spacing: 1px;
}
QPushButton#btn_pdf {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #F5C842, stop:1 #E8A020);
    color: #0D1117;
    border: none;
    border-radius: 10px;
    font-size: 13px;
    font-weight: bold;
    padding: 0px 24px;
    min-height: 42px;
    min-width: 170px;
}
QPushButton#btn_pdf:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #FFD55A, stop:1 #F0B030);
}
QPushButton#btn_pdf:disabled {
    background: rgba(255,255,255,0.08);
    color: rgba(255,255,255,0.2);
}
QPushButton#btn_back {
    background: transparent;
    color: rgba(255,255,255,0.4);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    font-size: 13px;
    padding: 0px 20px;
    min-height: 42px;
}
QPushButton#btn_back:hover {
    background: rgba(255,255,255,0.05);
    color: rgba(255,255,255,0.8);
}
/* ── Stat cards ──────────────────────────────── */
QWidget#stat_card {
    background: #13191F;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
}
QWidget#stat_card_active {
    background: rgba(245,200,66,0.08);
    border: 1px solid rgba(245,200,66,0.2);
    border-radius: 14px;
}
QLabel#stat_num {
    color: #F5C842;
    font-size: 28px;
    font-weight: bold;
}
QLabel#stat_lbl {
    color: rgba(255,255,255,0.4);
    font-size: 9px;
    letter-spacing: 2px;
}
/* ── Tabs ────────────────────────────────────── */
QTabWidget::pane {
    background: transparent;
    border: none;
}
QTabWidget::tab-bar { alignment: left; }
QTabBar::tab {
    background: transparent;
    color: rgba(255,255,255,0.35);
    padding: 12px 22px;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 1px;
    border: none;
    border-bottom: 2px solid transparent;
    margin-right: 4px;
}
QTabBar::tab:selected {
    color: #F5C842;
    border-bottom: 2px solid #F5C842;
}
QTabBar::tab:hover:!selected {
    color: rgba(255,255,255,0.7);
    background: rgba(255,255,255,0.03);
}
/* ── Tables ──────────────────────────────────── */
QTableWidget {
    background: #13191F;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    gridline-color: rgba(255,255,255,0.04);
    color: rgba(255,255,255,0.8);
    font-size: 12px;
    selection-background-color: rgba(245,200,66,0.1);
    selection-color: #FFFFFF;
    alternate-background-color: rgba(255,255,255,0.02);
}
QTableWidget::item { padding: 10px 12px; border: none; }
QTableWidget::item:selected { background: rgba(245,200,66,0.12); color: #FFFFFF; }
QHeaderView::section {
    background: #0D1117;
    color: rgba(255,255,255,0.35);
    font-weight: bold;
    font-size: 10px;
    letter-spacing: 2px;
    padding: 10px 12px;
    border: none;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
/* ── Warnings text ───────────────────────────── */
QTextEdit {
    background: #13191F;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    color: rgba(255,200,100,0.8);
    font-size: 12px;
    padding: 16px;
    font-family: 'Courier New';
}
"""


class AnalyseThread(QThread):
    termine = Signal(dict)
    erreur  = Signal(str)

    def __init__(self, chemin_ifc, nom_projet, nom_utilisateur):
        super().__init__()
        self.chemin_ifc      = chemin_ifc
        self.nom_projet      = nom_projet
        self.nom_utilisateur = nom_utilisateur

    def run(self):
        try:
            from src.analyseurs.parseurIfc import parseur
            rapport = parseur(self.chemin_ifc)
            self.termine.emit(rapport)
        except Exception as e:
            self.erreur.emit(str(e))


class ResultsWindow(QMainWindow):
    def __init__(self, chemin_ifc, nom_projet, utilisateur, dashboard_ref=None):
        super().__init__()
        self.chemin_ifc    = chemin_ifc
        self.nom_projet    = nom_projet
        self.utilisateur   = utilisateur
        self.dashboard_ref = dashboard_ref
        self.rapport       = None
        self.setWindowTitle(f"BATICALC — {nom_projet}")
        self.resize(1200, 780)
        self.setStyleSheet(STYLE)
        self._build_ui()
        self.center()
        self._lancer_analyse()

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(self.screen().availableGeometry().center())
        self.move(qr.topLeft())

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── TOP BAR ───────────────────────────────────
        topbar = QWidget()
        topbar.setObjectName("topbar")
        topbar.setFixedHeight(68)
        tb = QHBoxLayout(topbar)
        tb.setContentsMargins(28, 0, 28, 0)
        tb.setSpacing(16)

        brand = QLabel("BATICALC")
        brand.setObjectName("app_brand")
        tb.addWidget(brand)

        sep = QLabel("|")
        sep.setStyleSheet("color: rgba(255,255,255,0.15); font-size: 18px;")
        tb.addWidget(sep)

        self.lbl_title = QLabel("Analyse en cours...")
        self.lbl_title.setObjectName("result_title")
        tb.addWidget(self.lbl_title)

        tb.addStretch()

        self.lbl_projet = QLabel(f"  {self.nom_projet}")
        self.lbl_projet.setObjectName("project_name")
        tb.addWidget(self.lbl_projet)

        self.btn_pdf = QPushButton("  Télécharger PDF")
        self.btn_pdf.setObjectName("btn_pdf")
        self.btn_pdf.setCursor(Qt.PointingHandCursor)
        self.btn_pdf.setEnabled(False)
        tb.addWidget(self.btn_pdf)

        self.btn_back = QPushButton("← Retour")
        self.btn_back.setObjectName("btn_back")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        tb.addWidget(self.btn_back)

        root.addWidget(topbar)

        # ── STATS BAR ─────────────────────────────────
        stats_bar = QWidget()
        stats_bar.setStyleSheet("background: #0D1117; border-bottom: 1px solid rgba(255,255,255,0.06);")
        stats_bar.setFixedHeight(90)
        sb = QHBoxLayout(stats_bar)
        sb.setContentsMargins(28, 14, 28, 14)
        sb.setSpacing(16)

        self.stat_murs       = self._stat_card(sb, "0", "MURS")
        self.stat_fondations = self._stat_card(sb, "0", "FONDATIONS")
        self.stat_poteaux    = self._stat_card(sb, "0", "POTEAUX")
        self.stat_toitures   = self._stat_card(sb, "0", "TOITURES")
        sb.addStretch()

        # Animated loading bar
        self.loading_bar = QWidget()
        self.loading_bar.setFixedSize(200, 4)
        self.loading_bar.setStyleSheet("background: rgba(245,200,66,0.15); border-radius: 2px;")
        sb.addWidget(self.loading_bar, alignment=Qt.AlignVCenter)

        self.loading_inner = QWidget(self.loading_bar)
        self.loading_inner.setGeometry(0, 0, 0, 4)
        self.loading_inner.setStyleSheet("background: #F5C842; border-radius: 2px;")

        self._loading_val = 0
        self._loading_timer = QTimer()
        self._loading_timer.timeout.connect(self._tick_loading)
        self._loading_timer.start(30)

        root.addWidget(stats_bar)

        # ── TAB WIDGET ────────────────────────────────
        content_wrap = QWidget()
        content_wrap.setStyleSheet("background: #0A0F14;")
        cw = QVBoxLayout(content_wrap)
        cw.setContentsMargins(28, 24, 28, 24)

        self.tabs = QTabWidget()
        cw.addWidget(self.tabs)

        self.table_murs       = self._make_table(["Nom", "Type IFC", "Matériau", "Surface (m²)", "Volume (m³)", "Hauteur (m)"])
        self.table_fondations = self._make_table(["Nom", "Type", "Volume (m³)", "Surface base (m²)", "Hauteur (m)", "Coffrage (m²)"])
        self.table_poteaux    = self._make_table(["Nom", "Section", "Étage", "Hauteur (m)", "Volume (m³)", "Poids (kg)"])
        self.table_toitures   = self._make_table(["Nom", "Type objet", "Étage", "Surf. horiz. (m²)", "Surf. réelle (m²)", "Pente (°)"])
        self.text_erreurs     = QTextEdit()
        self.text_erreurs.setReadOnly(True)

        self.tabs.addTab(self._wrap_tab(self.table_murs),       "MURS")
        self.tabs.addTab(self._wrap_tab(self.table_fondations), "FONDATIONS")
        self.tabs.addTab(self._wrap_tab(self.table_poteaux),    "POTEAUX")
        self.tabs.addTab(self._wrap_tab(self.table_toitures),   "TOITURES")
        self.tabs.addTab(self._wrap_tab(self.text_erreurs),     "AVERTISSEMENTS")

        root.addWidget(content_wrap)

        self.btn_pdf.clicked.connect(self.on_exporter_pdf)
        self.btn_back.clicked.connect(self.on_retour)

    def _stat_card(self, layout, num, label):
        card = QWidget()
        card.setObjectName("stat_card")
        card.setFixedHeight(62)
        card.setMinimumWidth(140)
        h = QHBoxLayout(card)
        h.setContentsMargins(18, 0, 18, 0)
        h.setSpacing(12)
        num_lbl = QLabel(num)
        num_lbl.setObjectName("stat_num")
        lbl_lbl = QLabel(label)
        lbl_lbl.setObjectName("stat_lbl")
        h.addWidget(num_lbl)
        h.addWidget(lbl_lbl, alignment=Qt.AlignVCenter)
        layout.addWidget(card)
        return num_lbl

    def _wrap_tab(self, widget):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 16, 0, 0)
        v.addWidget(widget)
        return w

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
        for i in range(1, len(headers)):
            t.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        return t

    def _tick_loading(self):
        if self._loading_val < 190:
            self._loading_val += 2
            self.loading_inner.setFixedWidth(self._loading_val)

    # ── Analysis ──────────────────────────────────────────
    def _lancer_analyse(self):
        self.thread = AnalyseThread(self.chemin_ifc, self.nom_projet,
                                     self.utilisateur.get("nom", ""))
        self.thread.termine.connect(self._on_analyse_terminee)
        self.thread.erreur.connect(self._on_analyse_erreur)
        self.thread.start()

    def _on_analyse_terminee(self, rapport):
        self._loading_timer.stop()
        self.loading_inner.setFixedWidth(200)
        self.rapport = rapport
        self.lbl_title.setText("Résultats d'analyse IFC")
        self.stat_murs.setText(str(len(rapport.get("murs", []))))
        self.stat_fondations.setText(str(len(rapport.get("fondations", []))))
        self.stat_poteaux.setText(str(len(rapport.get("poteaux", []))))
        self.stat_toitures.setText(str(len(rapport.get("toitures", []))))
        self._fill_murs(rapport.get("murs", []))
        self._fill_fondations(rapport.get("fondations", []))
        self._fill_poteaux(rapport.get("poteaux", []))
        self._fill_toitures(rapport.get("toitures", []))
        erreurs = rapport.get("erreurs", [])
        self.text_erreurs.setPlainText("\n".join(erreurs) if erreurs else "Aucun avertissement.")
        self.btn_pdf.setEnabled(True)
        QTimer.singleShot(400, lambda: self.loading_bar.hide())

    def _on_analyse_erreur(self, msg):
        self._loading_timer.stop()
        self.lbl_title.setText("Erreur d'analyse")
        QMessageBox.critical(self, "Erreur", f"Analyse échouée :\n{msg}")

    def _fill(self, table, rows):
        table.setRowCount(0)
        for row_data in rows:
            r = table.rowCount()
            table.insertRow(r)
            for c, val in enumerate(row_data):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(r, c, item)

    def _fill_murs(self, murs):
        self._fill(self.table_murs, [
            [m.get("nom_instance","—"), m.get("type_ifc","—"), m.get("materiau","—"),
             f"{m.get('surface',0):.2f}", f"{m.get('volume',0):.3f}",
             f"{m.get('hauteur',0):.2f}"] for m in murs])

    def _fill_fondations(self, fonds):
        self._fill(self.table_fondations, [
            [f.get("nom_instance","—"), f.get("type_ifc","—"),
             f"{f.get('volume',0):.3f}", f"{f.get('surface_base',0):.2f}",
             f"{f.get('hauteur',0):.2f}", f"{f.get('surface_coffrage_lateral',0):.2f}"]
            for f in fonds])

    def _fill_poteaux(self, poteaux):
        self._fill(self.table_poteaux, [
            [p.get("nom","—"), p.get("materiau","—"), p.get("etage","—"),
             f"{p.get('hauteur',0):.2f}", f"{p.get('volume_net',0):.3f}",
             f"{p.get('poids_estime_kg',0):.0f}"] for p in poteaux])

    def _fill_toitures(self, toitures):
        self._fill(self.table_toitures, [
            [t.get("nom","—"), t.get("type_objet","—"), t.get("etage","—"),
             f"{t.get('surface_horizontale',0):.2f}", f"{t.get('surface_reelle',0):.2f}",
             f"{t.get('pente_moyenne',0):.1f}"] for t in toitures])

    # ── Export PDF ────────────────────────────────────────
    def on_exporter_pdf(self):
        if not self.rapport:
            return
        chemin, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le rapport PDF",
            f"BATICALC_{self.nom_projet}.pdf", "PDF (*.pdf)")
        if not chemin:
            return
        try:
            from src.export.pdf_exporter import exporter_pdf
            import shutil
            pdf = exporter_pdf(rapport=self.rapport, nom_projet=self.nom_projet,
                               nom_utilisateur=self.utilisateur.get("nom",""),
                               chemin_ifc=self.chemin_ifc,
                               output_dir=os.path.dirname(chemin))
            if pdf != chemin:
                shutil.move(pdf, chemin)
            QMessageBox.information(self, "PDF exporté", f"Rapport enregistré :\n{chemin}")
            import subprocess, platform
            if platform.system() == "Windows":
                os.startfile(chemin)
            elif platform.system() == "Darwin":
                subprocess.run(["open", chemin])
            else:
                subprocess.run(["xdg-open", chemin])
        except Exception as e:
            QMessageBox.critical(self, "Erreur export", f"Impossible de créer le PDF :\n{e}")

    def on_retour(self):
        if self.dashboard_ref:
            self.dashboard_ref.show()
            self.dashboard_ref._actualiser_projets()
        self.close()
