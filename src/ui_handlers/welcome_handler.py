# src/ui_handlers/welcome_handler.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                                QHBoxLayout, QLabel, QPushButton, QFrame)

STYLE = """
QMainWindow, QWidget { background: #0D1117; font-family: 'Segoe UI', sans-serif; }
QWidget#left_panel { background: #0D1117; border-right: 1px solid rgba(255,255,255,0.07); }
QWidget#right_panel { background: #13191F; }
QLabel#lbl_badge {
    color: #F5C842; font-size: 10px; font-weight: bold; letter-spacing: 4px;
}
QLabel#lbl_logo {
    color: #FFFFFF; font-size: 56px; font-weight: 900;
}
QFrame#accent_line { background: #F5C842; border-radius: 2px; }
QLabel#lbl_tagline {
    color: #FFFFFF; font-size: 22px; font-weight: bold;
}
QLabel#lbl_desc { color: #8892A4; font-size: 13px; }
QLabel#lbl_version { color: rgba(255,255,255,0.2); font-size: 11px; }
QLabel#lbl_welcome_title { color: #FFFFFF; font-size: 32px; font-weight: bold; }
QLabel#lbl_sub { color: #8892A4; font-size: 14px; }
QPushButton#btn_login {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #F5C842, stop:1 #E8A020);
    color: #0D1117; border: none; border-radius: 10px;
    font-size: 15px; font-weight: bold; min-height: 56px;
}
QPushButton#btn_login:hover { background: #FFD55A; }
QPushButton#btn_register {
    background: transparent; color: rgba(255,255,255,0.7);
    border: 1px solid rgba(255,255,255,0.15); border-radius: 10px;
    font-size: 15px; font-weight: 600; min-height: 56px;
}
QPushButton#btn_register:hover { border-color: #F5C842; color: #F5C842; }
QFrame#feat_line { background: #F5C842; border-radius: 2px; }
QLabel#feat_title { color: #FFFFFF; font-size: 13px; font-weight: bold; }
QLabel#feat_sub { color: #8892A4; font-size: 12px; }
"""


class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BATICALC")
        self.resize(960, 620)
        self.setStyleSheet(STYLE)
        self._build_ui()
        self.center()

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
        root.addWidget(self._left_panel(), 0)
        root.addWidget(self._right_panel(), 1)

    def _left_panel(self):
        panel = QWidget()
        panel.setObjectName("left_panel")
        panel.setFixedWidth(400)
        v = QVBoxLayout(panel)
        v.setContentsMargins(52, 60, 52, 52)
        v.setSpacing(0)

        badge = QLabel("LOGICIEL BIM")
        badge.setObjectName("lbl_badge")
        v.addWidget(badge)
        v.addSpacing(28)

        logo = QLabel("BATI\nCALC")
        logo.setObjectName("lbl_logo")
        v.addWidget(logo)
        v.addSpacing(20)

        line = QFrame()
        line.setObjectName("accent_line")
        line.setFixedSize(64, 4)
        v.addWidget(line)
        v.addSpacing(20)

        tag = QLabel("Calculez. Mesurez.\nConstruisez mieux.")
        tag.setObjectName("lbl_tagline")
        tag.setWordWrap(True)
        v.addWidget(tag)
        v.addSpacing(16)

        desc = QLabel("Analyse automatique de fichiers IFC\npour estimer les quantites de Gros\nOeuvre en quelques secondes.")
        desc.setObjectName("lbl_desc")
        desc.setWordWrap(True)
        v.addWidget(desc)
        v.addStretch()

        ver = QLabel("v1.0 — Yaounde, Cameroun")
        ver.setObjectName("lbl_version")
        v.addWidget(ver)
        return panel

    def _right_panel(self):
        panel = QWidget()
        panel.setObjectName("right_panel")
        v = QVBoxLayout(panel)
        v.setContentsMargins(60, 0, 60, 0)
        v.setSpacing(0)
        v.addStretch()

        title = QLabel("Bienvenue")
        title.setObjectName("lbl_welcome_title")
        v.addWidget(title)
        v.addSpacing(8)

        sub = QLabel("Connectez-vous ou creez un compte\npour commencer votre analyse.")
        sub.setObjectName("lbl_sub")
        sub.setWordWrap(True)
        v.addWidget(sub)
        v.addSpacing(40)

        self.btn_login = QPushButton("Se connecter")
        self.btn_login.setObjectName("btn_login")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        v.addWidget(self.btn_login)
        v.addSpacing(14)

        self.btn_register = QPushButton("Creer un compte")
        self.btn_register.setObjectName("btn_register")
        self.btn_register.setCursor(Qt.PointingHandCursor)
        v.addWidget(self.btn_register)
        v.addSpacing(40)

        for titre, detail in [
            ("Analyse IFC rapide", "Murs, fondations, poteaux, toitures"),
            ("Export PDF professionnel", "Tableau de metre complet"),
        ]:
            row = QHBoxLayout()
            row.setSpacing(14)
            fl = QFrame()
            fl.setObjectName("feat_line")
            fl.setFixedSize(3, 40)
            row.addWidget(fl)
            col = QVBoxLayout()
            col.setSpacing(2)
            ft = QLabel(titre)
            ft.setObjectName("feat_title")
            fs = QLabel(detail)
            fs.setObjectName("feat_sub")
            col.addWidget(ft)
            col.addWidget(fs)
            row.addLayout(col)
            v.addLayout(row)
            v.addSpacing(14)

        v.addStretch()

        self.btn_login.clicked.connect(self.on_login)
        self.btn_register.clicked.connect(self.on_register)
        return panel

    def on_login(self):
        from src.ui_handlers.login_handler import LoginWindow
        self.login = LoginWindow()
        self.login.show()
        self.close()

    def on_register(self):
        from src.ui_handlers.register_handler import RegisterWindow
        self.register = RegisterWindow()
        self.register.show()
        self.close()
