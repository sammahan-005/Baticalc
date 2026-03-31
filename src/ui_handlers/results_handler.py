# src/ui_handlers/results_handler.py
import os
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (QMainWindow, QTableWidgetItem,
                                QHeaderView, QMessageBox, QFileDialog)
from generated.ui_results import Ui_ResultsWindow

HEADER_STYLE = """
    QWidget#headerBar { background-color: #2c3e50; }
    QLabel#label_titre { color: white; font-size: 18px; font-weight: bold; }
    QLabel#label_nom_projet { color: #bdc3c7; font-size: 12px; }
    QPushButton#btn_exporter_pdf {
        background-color: #e74c3c; color: white; border: none;
        border-radius: 5px; font-size: 13px; font-weight: bold; padding: 8px 16px; }
    QPushButton#btn_exporter_pdf:hover { background-color: #c0392b; }
    QPushButton#btn_retour {
        background-color: transparent; color: #bdc3c7;
        border: 1px solid #7f8c8d; border-radius: 5px;
        font-size: 13px; padding: 8px 12px; }
    QPushButton#btn_retour:hover { color: white; border-color: white; }
"""
STATS_STYLE = """
    QWidget#statsBar { background-color: #f0f3f7; }
    QFrame { background-color: white; border-radius: 8px; border: 1px solid #ecf0f1; }
    QLabel#label_nb_murs, QLabel#label_nb_fondations,
    QLabel#label_nb_poteaux, QLabel#label_nb_toitures {
        color: #3498db; font-size: 20px; font-weight: bold; }
    QLabel#label_nb_murs_txt, QLabel#label_nb_fondations_txt,
    QLabel#label_nb_poteaux_txt, QLabel#label_nb_toitures_txt {
        color: #7f8c8d; font-size: 11px; }
"""
TABLE_STYLE = """
    QTableWidget { background-color: white; border: none;
        gridline-color: #ecf0f1; font-size: 12px; color: #2c3e50; }
    QTableWidget::item:selected { background-color: #d6eaf8; color: #2c3e50; }
    QHeaderView::section { background-color: #2c3e50; color: white;
        font-weight: bold; font-size: 11px; padding: 8px; border: none; }
    QTabWidget::pane { border: none; background: #f0f3f7; }
    QTabBar::tab { background: #ecf0f1; color: #7f8c8d;
        padding: 10px 20px; font-size: 12px; border: none; margin-right: 2px; }
    QTabBar::tab:selected { background: #3498db; color: white; font-weight: bold; }
"""


# ── Background analysis thread ────────────────────────────────────────────────

class AnalyseThread(QThread):
    termine  = Signal(dict)
    erreur   = Signal(str)

    def __init__(self, chemin_ifc, nom_projet, nom_utilisateur):
        super().__init__()
        self.chemin_ifc     = chemin_ifc
        self.nom_projet     = nom_projet
        self.nom_utilisateur = nom_utilisateur

    def run(self):
        try:
            from src.analyseurs.parseurIfc import parseur
            rapport = parseur(self.chemin_ifc)
            self.termine.emit(rapport)
        except Exception as e:
            self.erreur.emit(str(e))


# ── Results window ──────────────────────────────────────────────────────────

class ResultsWindow(QMainWindow):
    def __init__(self, chemin_ifc: str, nom_projet: str,
                 utilisateur: dict, dashboard_ref=None):
        super().__init__()
        self.chemin_ifc    = chemin_ifc
        self.nom_projet    = nom_projet
        self.utilisateur   = utilisateur
        self.dashboard_ref = dashboard_ref
        self.rapport       = None

        self.ui = Ui_ResultsWindow()
        self.ui.setupUi(self)
        self.resize(1100, 750)
        self.center()

        self.ui.headerBar.setStyleSheet(HEADER_STYLE)
        self.ui.statsBar.setStyleSheet(STATS_STYLE)
        self.ui.tabWidget.setStyleSheet(TABLE_STYLE)
        self.ui.label_nom_projet.setText(f"Projet : {nom_projet}")
        self.ui.btn_exporter_pdf.setEnabled(False)

        self._setup_tables()
        self.ui.btn_exporter_pdf.clicked.connect(self.on_exporter_pdf)
        self.ui.btn_retour.clicked.connect(self.on_retour)

        self._lancer_analyse()

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(self.screen().availableGeometry().center())
        self.move(qr.topLeft())

    def _setup_tables(self):
        self.ui.table_murs.setHorizontalHeaderLabels(
            ["Nom", "Type IFC", "Surface (m2)", "Volume (m3)", "Hauteur (m)"])
        self.ui.table_fondations.setHorizontalHeaderLabels(
            ["Nom", "Type", "Volume (m3)", "Surface (m2)", "Hauteur (m)", "Perimetre (m)"])
        self.ui.table_poteaux.setHorizontalHeaderLabels(
            ["Nom", "Materiau","Niveau", "Hauteur (m)", "Volume (m3)","Surface section (m2)"])
        self.ui.table_toitures.setHorizontalHeaderLabels(
            ["Nom", "Type", "Surface horizontale (m2)", "Surface reelle (m2)", "Pente"])

        for table in [self.ui.table_murs, self.ui.table_fondations,
                      self.ui.table_poteaux, self.ui.table_toitures]:
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            for c in range(1, table.columnCount()):
                table.horizontalHeader().setSectionResizeMode(c, QHeaderView.ResizeToContents)
            table.verticalHeader().setVisible(False)

    # ── Analysis ─────────────────────────────────────────────────────────────

    def _lancer_analyse(self):
        self.ui.label_titre.setText("Analyse en cours...")
        self.ui.btn_exporter_pdf.setEnabled(False)
        self.thread = AnalyseThread(
            self.chemin_ifc, self.nom_projet,
            self.utilisateur.get("nom", "")
        )
        self.thread.termine.connect(self._on_analyse_terminee)
        self.thread.erreur.connect(self._on_analyse_erreur)
        self.thread.start()

    def _on_analyse_terminee(self, rapport):
        self.rapport = rapport
        self.ui.label_titre.setText("Resultats d'analyse IFC")
        self._remplir_stats(rapport)
        self._remplir_murs(rapport.get("murs", []))
        self._remplir_fondations(rapport.get("fondations", []))
        self._remplir_poteaux(rapport.get("poteaux", []))
        self._remplir_toitures(rapport.get("toitures", []))
        erreurs = rapport.get("erreurs", [])
        self.ui.text_erreurs.setPlainText(
            "\n".join(erreurs) if erreurs else "Aucun avertissement.")
        self.ui.btn_exporter_pdf.setEnabled(True)

    def _on_analyse_erreur(self, msg):
        self.ui.label_titre.setText("Erreur d'analyse")
        QMessageBox.critical(self, "Erreur", f"Analyse echouee :\n{msg}")

    # ── Fill tables ───────────────────────────────────────────────────────────

    def _remplir_stats(self, r):
        self.ui.label_nb_murs.setText(str(len(r.get("murs", []))))
        self.ui.label_nb_fondations.setText(str(len(r.get("fondations", []))))
        self.ui.label_nb_poteaux.setText(str(len(r.get("poteaux", []))))
        self.ui.label_nb_toitures.setText(str(len(r.get("toitures", []))))

    def _fill_table(self, table, rows):
        table.setRowCount(0)
        for row_data in rows:
            row = table.rowCount()
            table.insertRow(row)
            for col, val in enumerate(row_data):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, col, item)

    def _remplir_murs(self, murs):
        self._fill_table(self.ui.table_murs, [
            [m.get("nom_instance","—"), m.get("type_ifc","—"),
             f"{m.get('surface',0):.3f}", f"{m.get('volume',0):.3f}",
             f"{m.get('hauteur',0):.2f}"] for m in murs])

    def _remplir_fondations(self, fondations):
        self._fill_table(self.ui.table_fondations, [
            [f.get("nom_instance","—"),f"{f.get("type_ifc","—")}",
             f"{f.get('volume',0):.3f}", f"{f.get('surface_base',0):.3f}",
             f"{f.get('hauteur',0):.3f}",f"{f.get('perimetre',0):.3f}"]
            for f in fondations])

    def _remplir_poteaux(self, poteaux):
        self._fill_table(self.ui.table_poteaux, [
            [p.get("nom","—"),p.get("etage","—"),p.get("materiau","—"),
             f"{p.get('hauteur',0):.2f}", f"{p.get('volume_net',0):.3f}",
             f"{p.get('surface_section',0):.3f}"] for p in poteaux])

    def _remplir_toitures(self, toitures):
        self._fill_table(self.ui.table_toitures, [
            [t.get("nom_instance","—"), t.get("type_ifc","—"),
             f"{t.get('surface_horizontale',0):.3f}", f"{t.get('surface_reele',0):.3f}",
             f"{t.get('pente_moyenne',0):.1f}"] for t in toitures])

    # ── Export PDF ────────────────────────────────────────────────────────────

    def on_exporter_pdf(self):
        if not self.rapport:
            return
        chemin, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le rapport PDF",
            f"BATICALC_{self.nom_projet}.pdf",
            "Fichiers PDF (*.pdf)")
        if not chemin:
            return
        try:
            from src.export.pdf_exporter import exporter_pdf
            pdf = exporter_pdf(
                rapport=self.rapport,
                nom_projet=self.nom_projet,
                nom_utilisateur=self.utilisateur.get("nom", ""),
                chemin_ifc=self.chemin_ifc,
                output_dir=os.path.dirname(chemin)
            )
            import shutil
            if pdf != chemin:
                shutil.move(pdf, chemin)
            QMessageBox.information(self, "PDF exporte",
                                    f"Rapport enregistre :\n{chemin}")
            import subprocess, platform
            if platform.system() == "Windows":
                os.startfile(chemin)
            elif platform.system() == "Darwin":
                subprocess.run(["open", chemin])
            else:
                subprocess.run(["xdg-open", chemin])
        except Exception as e:
            QMessageBox.critical(self, "Erreur export",
                                 f"Impossible de creer le PDF :\n{e}")

    def on_retour(self):
        if self.dashboard_ref:
            self.dashboard_ref.show()
            self.dashboard_ref._actualiser_projets()
        self.close()