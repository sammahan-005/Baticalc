# src/ui_handlers/register_handler.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                                QHBoxLayout, QLabel, QPushButton, QLineEdit)
from src.authentification import inscrire_utilisateur

STYLE = """
QMainWindow, QWidget { background: #0D1117; font-family: 'Segoe UI', sans-serif; }
QWidget#left_panel { background: #0D1117; border-right: 1px solid rgba(255,255,255,0.07); }
QWidget#right_panel { background: #13191F; }
QLabel#lbl_logo { color: #F5C842; font-size: 17px; font-weight: 900; letter-spacing: 3px; }
QLabel#lbl_hero { color: #FFFFFF; font-size: 28px; font-weight: bold; }
QLabel#lbl_hero_sub { color: #8892A4; font-size: 13px; }
QLabel#lbl_have_acct { color: rgba(255,255,255,0.3); font-size: 12px; }
QPushButton#btn_goto_login {
    background: transparent; color: #F5C842;
    border: 1px solid rgba(245,200,66,0.3); border-radius: 8px;
    font-size: 13px; font-weight: 600; min-height: 44px;
}
QPushButton#btn_goto_login:hover { background: rgba(245,200,66,0.08); border-color: #F5C842; }
QPushButton#btn_back {
    background: transparent; color: rgba(255,255,255,0.3);
    border: none; font-size: 12px; text-align: left;
}
QPushButton#btn_back:hover { color: rgba(255,255,255,0.7); }
QLabel#lbl_form_title { color: #FFFFFF; font-size: 26px; font-weight: bold; }
QLabel#form_label {
    color: rgba(255,255,255,0.35); font-size: 10px;
    font-weight: bold; letter-spacing: 2px;
}
QLabel#lbl_error { color: #FC8181; font-size: 12px; }
QLineEdit {
    background: rgba(255,255,255,0.05); color: #FFFFFF;
    border: 1px solid rgba(255,255,255,0.1); border-radius: 8px;
    padding: 0 16px; font-size: 14px; min-height: 50px;
    selection-background-color: #F5C842; selection-color: #0D1117;
}
QLineEdit:focus { border: 1px solid #F5C842; background: rgba(245,200,66,0.05); }
QPushButton#btn_register {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #F5C842, stop:1 #E8A020);
    color: #0D1117; border: none; border-radius: 10px;
    font-size: 15px; font-weight: bold; min-height: 54px;
}
QPushButton#btn_register:hover { background: #FFD55A; }
QPushButton#btn_register:disabled { background: rgba(255,255,255,0.07); color: rgba(255,255,255,0.25); }
"""


class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BATICALC — Inscription")
        self.resize(860, 640)
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
        root.addWidget(self._left_panel())
        root.addWidget(self._right_panel(), 1)

    def _left_panel(self):
        panel = QWidget()
        panel.setObjectName("left_panel")
        panel.setFixedWidth(320)
        v = QVBoxLayout(panel)
        v.setContentsMargins(40, 48, 40, 48)
        v.setSpacing(0)

        logo = QLabel("BATICALC")
        logo.setObjectName("lbl_logo")
        v.addWidget(logo)
        v.addStretch()

        hero = QLabel("Rejoignez\nBATICALC.")
        hero.setObjectName("lbl_hero")
        hero.setWordWrap(True)
        v.addWidget(hero)
        v.addSpacing(12)

        sub = QLabel("Creez votre compte gratuit et\ncommencez a analyser vos\nfichiers IFC immediatement.")
        sub.setObjectName("lbl_hero_sub")
        sub.setWordWrap(True)
        v.addWidget(sub)
        v.addStretch()

        have_acct = QLabel("Deja un compte ?")
        have_acct.setObjectName("lbl_have_acct")
        v.addWidget(have_acct)
        v.addSpacing(8)

        self.btn_goto_login = QPushButton("Se connecter")
        self.btn_goto_login.setObjectName("btn_goto_login")
        self.btn_goto_login.setCursor(Qt.PointingHandCursor)
        v.addWidget(self.btn_goto_login)
        v.addSpacing(12)

        self.btn_back = QPushButton("← Retour a l'accueil")
        self.btn_back.setObjectName("btn_back")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        v.addWidget(self.btn_back)
        return panel

    def _right_panel(self):
        panel = QWidget()
        panel.setObjectName("right_panel")
        v = QVBoxLayout(panel)
        v.setContentsMargins(56, 0, 56, 0)
        v.setSpacing(0)
        v.addStretch()

        title = QLabel("Creer un compte")
        title.setObjectName("lbl_form_title")
        v.addWidget(title)
        v.addSpacing(28)

        fields = [
            ("NOM COMPLET",             "input_nom",     "Jean Dupont",        False),
            ("ADRESSE EMAIL",           "input_email",   "vous@exemple.com",   False),
            ("MOT DE PASSE",            "input_mdp",     "Min. 6 caracteres",  True),
            ("CONFIRMER MOT DE PASSE",  "input_confirm", "••••••••••",         True),
        ]
        for label_text, attr, placeholder, is_pw in fields:
            v.addWidget(self._form_label(label_text))
            v.addSpacing(8)
            field = QLineEdit()
            field.setPlaceholderText(placeholder)
            field.setFocusPolicy(Qt.StrongFocus)
            if is_pw:
                field.setEchoMode(QLineEdit.Password)
            setattr(self, attr, field)
            v.addWidget(field)
            v.addSpacing(16)

        self.lbl_error = QLabel("")
        self.lbl_error.setObjectName("lbl_error")
        self.lbl_error.setWordWrap(True)
        v.addWidget(self.lbl_error)
        v.addSpacing(16)

        self.btn_register = QPushButton("Creer mon compte  →")
        self.btn_register.setObjectName("btn_register")
        self.btn_register.setCursor(Qt.PointingHandCursor)
        v.addWidget(self.btn_register)
        v.addStretch()

        self.btn_register.clicked.connect(self.on_register)
        self.btn_goto_login.clicked.connect(self.on_goto_login)
        self.btn_back.clicked.connect(self.on_back)
        return panel

    def _form_label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("form_label")
        return lbl

    def on_register(self):
        nom     = self.input_nom.text().strip()
        email   = self.input_email.text().strip()
        mdp     = self.input_mdp.text().strip()
        confirm = self.input_confirm.text().strip()
        if not nom or not email or not mdp or not confirm:
            self.lbl_error.setText("Veuillez remplir tous les champs.")
            return
        if mdp != confirm:
            self.lbl_error.setText("Les mots de passe ne correspondent pas.")
            return
        if len(mdp) < 6:
            self.lbl_error.setText("Mot de passe trop court (min. 6 caracteres).")
            return
        res = inscrire_utilisateur(nom, email, mdp)
        if res["succes"]:
            self.on_goto_login()
        else:
            self.lbl_error.setText(res["erreur"])

    def on_goto_login(self):
        from src.ui_handlers.login_handler import LoginWindow
        self.login = LoginWindow()
        self.login.show()
        self.close()

    def on_back(self):
        from src.ui_handlers.welcome_handler import WelcomeWindow
        self.welcome = WelcomeWindow()
        self.welcome.show()
        self.close()
