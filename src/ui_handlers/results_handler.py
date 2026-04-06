# src/ui_handlers/results_handler.py
import os
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                                QHeaderView, QTabWidget, QTextEdit, QMessageBox,
                                QFileDialog)

STYLE = """
QMainWindow, QWidget {
    background: #0A0F14;
    font-family: 'Segoe UI', sans-serif;
}
QWidget#topbar {
    background: #0D1117;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
QLabel#app_brand {
    color: #F5C842;
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 3px;
}
QLabel#result_title {
    color: #FFFFFF;
    font-size: 18px;
    font-weight: bold;
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
QWidget#stat_card {
    background: #13191F;
    border: 1px solid rgba(255,255,255,0.07);
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


# ── Background thread ────────────────────────────────────────────────────────

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


# ── Results window ───────────────────────────────────────────────────────────

class ResultsWindow(QMainWindow):
    def __init__(self, chemin_ifc, nom_projet, utilisateur, dashboard_ref=None):
        super().__init__()
        self.chemin_ifc    = chemin_ifc
        self.nom_projet    = nom_projet
        self.utilisateur   = utilisateur
        self.dashboard_ref = dashboard_ref
        self.rapport       = None
        self.resultat_devis = None
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

    # ── Build UI ─────────────────────────────────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # TOP BAR
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

        self.lbl_project = QLabel(f"  {self.nom_projet}  ")
        self.lbl_project.setObjectName("project_name")
        tb.addWidget(self.lbl_project)

        self.btn_pdf = QPushButton("  Telecharger PDF")
        self.btn_pdf.setObjectName("btn_pdf")
        self.btn_pdf.setCursor(Qt.PointingHandCursor)
        self.btn_pdf.setEnabled(False)
        tb.addWidget(self.btn_pdf)

        self.btn_back = QPushButton("← Retour")
        self.btn_back.setObjectName("btn_back")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        tb.addWidget(self.btn_back)

        root.addWidget(topbar)

        # STATS BAR
        stats_bar = QWidget()
        stats_bar.setStyleSheet(
            "background: #0D1117; border-bottom: 1px solid rgba(255,255,255,0.06);"
        )
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
        self.loading_bar.setStyleSheet(
            "background: rgba(245,200,66,0.15); border-radius: 2px;"
        )
        sb.addWidget(self.loading_bar, alignment=Qt.AlignVCenter)

        self.loading_inner = QWidget(self.loading_bar)
        self.loading_inner.setGeometry(0, 0, 0, 4)
        self.loading_inner.setStyleSheet("background: #F5C842; border-radius: 2px;")

        self._loading_val = 0
        self._loading_timer = QTimer()
        self._loading_timer.timeout.connect(self._tick_loading)
        self._loading_timer.start(30)

        root.addWidget(stats_bar)

        # TAB WIDGET
        content_wrap = QWidget()
        content_wrap.setStyleSheet("background: #0A0F14;")
        cw = QVBoxLayout(content_wrap)
        cw.setContentsMargins(28, 24, 28, 24)

        self.tabs = QTabWidget()
        cw.addWidget(self.tabs)

        self.table_murs = self._make_table(
            ["Nom", "Type IFC", "Surface (m2)", "Volume (m3)", "Hauteur (m)"])
        self.table_fondations = self._make_table(
            ["Nom", "Type", "Volume (m3)", "Surface (m2)", "Hauteur (m)", "Perimetre (m)"])
        self.table_poteaux = self._make_table(
            ["Nom", "Etage", "Materiau", "Hauteur (m)", "Volume (m3)", "Section (m2)"])
        self.table_toitures = self._make_table(
            ["Nom", "Type", "Etage", "Surf. horiz. (m2)", "Surf. reelle (m2)", "Pente"])
        self.text_erreurs = QTextEdit()
        self.text_erreurs.setReadOnly(True)

        self.tabs.addTab(self._wrap_tab(self.table_murs),       "MURS")
        self.tabs.addTab(self._wrap_tab(self.table_fondations), "FONDATIONS")
        self.tabs.addTab(self._wrap_tab(self.table_poteaux),    "POTEAUX")
        self.tabs.addTab(self._wrap_tab(self.table_toitures),   "TOITURES")
        self.tabs.addTab(self._wrap_tab(self.text_erreurs),     "AVERTISSEMENTS")

        root.addWidget(content_wrap)

        # Connect buttons
        self.btn_pdf.clicked.connect(self.on_exporter_pdf)
        self.btn_back.clicked.connect(self.on_retour)

    # ── Helpers ──────────────────────────────────────────────────────────────

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

    # ── Analysis ─────────────────────────────────────────────────────────────

    def _lancer_analyse(self):
        self.thread = AnalyseThread(
            self.chemin_ifc, self.nom_projet,
            self.utilisateur.get("nom", "")
        )
        self.thread.termine.connect(self._on_analyse_terminee)
        self.thread.erreur.connect(self._on_analyse_erreur)
        self.thread.start()

    def _on_analyse_terminee(self, rapport):
        self._loading_timer.stop()
        self.loading_inner.setFixedWidth(200)
        self.rapport = rapport
        self.lbl_title.setText("Resultats d'analyse IFC")
        self.stat_murs.setText(str(len(rapport.get("murs", []))))
        self.stat_fondations.setText(str(len(rapport.get("fondations", []))))
        self.stat_poteaux.setText(str(len(rapport.get("poteaux", []))))
        self.stat_toitures.setText(str(len(rapport.get("toitures", []))))
        self._fill_murs(rapport.get("murs", []))
        self._fill_fondations(rapport.get("fondations", []))
        self._fill_poteaux(rapport.get("poteaux", []))
        self._fill_toitures(rapport.get("toitures", []))
        erreurs = rapport.get("erreurs", [])
        self.text_erreurs.setPlainText(
            "\n".join(erreurs) if erreurs else "Aucun avertissement."
        )
        self.btn_pdf.setEnabled(True)
        QTimer.singleShot(400, lambda: self.loading_bar.hide())
        self._sauvegarder_et_calculer()

    def _on_analyse_erreur(self, msg):
        self._loading_timer.stop()
        self.lbl_title.setText("Erreur d'analyse")
        QMessageBox.critical(self, "Erreur", f"Analyse echouee :\n{msg}")

    # ── Fill tables ───────────────────────────────────────────────────────────

    def _fill(self, table, rows):
        table.setRowCount(0)
        for row_data in rows:
            r = table.rowCount()
            table.insertRow(r)
            table.setRowHeight(r, 44)
            for c, val in enumerate(row_data):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(r, c, item)

    def _fill_murs(self, murs):
        self._fill(self.table_murs, [
            [m.get("nom_instance", "-"),
             m.get("type_ifc", "-"),
             f"{m.get('surface', 0):.3f}",
             f"{m.get('volume', 0):.3f}",
             f"{m.get('hauteur', 0):.2f}"]
            for m in murs
        ])

    def _fill_fondations(self, fondations):
        self._fill(self.table_fondations, [
            [f.get("nom_instance", "-"),
             f.get("type_ifc", "-"),
             f"{f.get('volume', 0):.3f}",
             f"{f.get('surface_base', 0):.3f}",
             f"{f.get('hauteur', 0):.3f}",
             f"{f.get('perimetre', 0):.3f}"]
            for f in fondations
        ])

    def _fill_poteaux(self, poteaux):
        self._fill(self.table_poteaux, [
            [p.get("nom", "-"),
             p.get("etage", "-"),
             p.get("materiau", "-"),
             f"{p.get('hauteur', 0):.2f}",
             f"{p.get('volume_net', 0):.3f}",
             f"{p.get('surface_section', 0):.3f}"]
            for p in poteaux
        ])

    def _fill_toitures(self, toitures):
        self._fill(self.table_toitures, [
            [t.get("nom_instance", "-"),
             t.get("type_ifc", "-"),
             t.get("etage", "-"),
             f"{t.get('surface_horizontale', 0):.3f}",
             f"{t.get('surface_reelle', 0):.3f}",
             f"{t.get('pente_moyenne', 0):.1f}"]
            for t in toitures
        ])

    # ── Devis calculation ─────────────────────────────────────────────────────

    def _sauvegarder_et_calculer(self):
        """Save results to DB (marks project as termine) then compute devis."""
        try:
            import session
            projet_id = session.projet_actuel.get("id")
            if projet_id and self.rapport:
                from src.base_de_donnees import sauvegarder_resultats_ifc
                sauvegarder_resultats_ifc(projet_id, self.rapport)
        except Exception as e:
            pass  # Non-fatal: UI still works even if DB save fails
        self._calculer_devis()

    def _calculer_devis(self):
        """Compute resultat_devis from the current rapport using the calculateur."""
        try:
            import session
            projet_id = session.projet_actuel.get("id")
            if not projet_id:
                return

            from src.calculateur.calculateur import (
                generer_synthese_projet, convertir_en_materiaux_et_estimer
            )

            synthese = generer_synthese_projet(projet_id)

            # Prix du marché Cameroun (Yaoundé/Douala) — référence 2024-2025
            prix_ref = [
                ("Sacs ciment 50kg",        5400,   "sac"),     # Cimencam/Lafarge ~5 400 FCFA
                ("Sable (m3)",              9000,   "m3"),      # Camion 20t=180 000 FCFA → ~9 000/m3
                ("Gravier (m3)",            10000,  "m3"),     # Camion 20t à 145 000 FCFA → ~7 250/t, ~10 000/m3
                ("Sable fin (m3)",          10000,  "m3"),     # Sable fin carrière ≈ 10 000 FCFA/m3
                ("Barres HA06 (6m)",        1500,   "barre"),  # Barre HA6 6m ≈ 1 500 FCFA
                ("Barres HA08 (12m)",       3055,   "barre"),  # HA8 12m Yaoundé ≈ 3 055 FCFA
                ("Barres HA10 (12m)",       4680,   "barre"),  # HA10 12m Yaoundé ≈ 4 680 FCFA
                ("Barres HA12 (12m)",       6725,   "barre"),  # HA12 12m Yaoundé ≈ 6 725 FCFA
                ("Parpaings 20x20x40",      280,    "parpaing"), # Parpaing 20cm ≈ 280 FCFA/pièce
                ("Bac acier / couverture",  6500,   "m2"),     # Tôle bac ALUCAM/SOCATRAL ≈ 6 500 FCFA/m2
                ("Bois charpente (m3)",     200000, "m3"),     # Bois charpente locale ≈ 200 000 FCFA/m3
                ("Clous / visserie (kg)",   1500,   "kg"),     # Clous/visserie ≈ 1 500 FCFA/kg
            ]

            self.resultat_devis = convertir_en_materiaux_et_estimer(synthese, prix_ref)

        except Exception as e:
            # Non-fatal: devis won't export but analysis PDF still works
            self.resultat_devis = None

    # ── Export PDF ────────────────────────────────────────────────────────────

    def on_exporter_pdf(self):
        if not self.rapport:
            return

        import shutil, subprocess, platform

        # Ask once: does the user want the analysis report or the devis?
        if self.resultat_devis:
            from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
            dlg = QDialog(self)
            dlg.setWindowTitle("Type de PDF")
            dlg.setStyleSheet("background:#0D1117; color:white;")
            v = QVBoxLayout(dlg)
            v.addWidget(QLabel("Quel document voulez-vous exporter ?"))
            h = QHBoxLayout()
            btn_rapport = QPushButton("Rapport d'analyse")
            btn_devis   = QPushButton("Devis matériaux")
            btn_rapport.setCursor(Qt.PointingHandCursor)
            btn_devis.setCursor(Qt.PointingHandCursor)
            h.addWidget(btn_rapport)
            h.addWidget(btn_devis)
            v.addLayout(h)
            choice = {"val": None}
            btn_rapport.clicked.connect(lambda: (choice.update(val="rapport"), dlg.accept()))
            btn_devis.clicked.connect(lambda:   (choice.update(val="devis"),   dlg.accept()))
            dlg.exec()
            if choice["val"] is None:
                return
            export_type = choice["val"]
        else:
            export_type = "rapport"

        if export_type == "rapport":
            chemin, _ = QFileDialog.getSaveFileName(
                self, "Enregistrer le rapport PDF",
                f"BATICALC_{self.nom_projet}.pdf", "PDF (*.pdf)"
            )
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
                if pdf != chemin:
                    shutil.move(pdf, chemin)
                QMessageBox.information(self, "PDF exporté", f"Rapport enregistré :\n{chemin}")
                if platform.system() == "Windows":
                    os.startfile(chemin)
                elif platform.system() == "Darwin":
                    subprocess.run(["open", chemin])
                else:
                    subprocess.run(["xdg-open", chemin])
            except Exception as e:
                QMessageBox.critical(self, "Erreur export", f"Impossible de créer le PDF :\n{e}")

        else:  # devis
            chemin, _ = QFileDialog.getSaveFileName(
                self, "Enregistrer le devis PDF",
                f"BATICALC_DEVIS_{self.nom_projet}.pdf", "PDF (*.pdf)"
            )
            if not chemin:
                return
            try:
                from src.export.exporter_devis_pdf import exporter_devis_pdf
                pdf = exporter_devis_pdf(
                    resultat_devis=self.resultat_devis,
                    nom_projet=self.nom_projet,
                    nom_utilisateur=self.utilisateur.get("nom", ""),
                    chemin_ifc=self.chemin_ifc,
                    output_dir=os.path.dirname(chemin)
                )
                if pdf != chemin:
                    shutil.move(pdf, chemin)
                QMessageBox.information(self, "PDF exporté", f"Devis enregistré :\n{chemin}")
                if platform.system() == "Windows":
                    os.startfile(chemin)
                elif platform.system() == "Darwin":
                    subprocess.run(["open", chemin])
                else:
                    subprocess.run(["xdg-open", chemin])
            except Exception as e:
                QMessageBox.critical(self, "Erreur export", f"Impossible de créer le devis PDF :\n{e}")

    # ── Back ──────────────────────────────────────────────────────────────────

    def on_retour(self):
        if self.dashboard_ref:
            self.dashboard_ref.show()
            self.dashboard_ref._actualiser_projets()
        self.close()