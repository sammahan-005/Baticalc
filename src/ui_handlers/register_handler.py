# src/ui_handlers/register_handler.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow
from generated.ui_register import Ui_RegisterWindow
from src.authentification import inscrire_utilisateur

FIELD = """
    QLineEdit {
        border: 2px solid #bdc3c7; border-radius: 5px;
        padding: 8px 12px; font-size: 14px;
        background-color: white; color: #2c3e50;
    }
    QLineEdit:focus { border: 2px solid #2ecc71; }
"""
STYLE = """
    QWidget { background-color: #f5f5f5; }
    QLabel#label_title    { color: #2c3e50; font-size: 36px; font-weight: bold; }
    QLabel#label_subtitle { color: #7f8c8d; font-size: 14px; }
    QLabel#label_nom, QLabel#label_email,
    QLabel#label_mdp, QLabel#label_confirm { color: #34495e; font-size: 13px; font-weight: bold; }
    QLabel#label_error { color: #e74c3c; font-size: 13px; }
    QLabel#label_sep   { color: #7f8c8d; font-size: 13px; }
    QPushButton#btn_register {
        background-color: #2ecc71; color: white; border: none;
        border-radius: 5px; font-size: 16px; font-weight: bold;
    }
    QPushButton#btn_register:hover { background-color: #27ae60; }
    QPushButton#btn_goto_login {
        background-color: white; color: #3498db;
        border: 2px solid #3498db; border-radius: 5px;
        font-size: 16px; font-weight: bold;
    }
    QPushButton#btn_goto_login:hover { background-color: #3498db; color: white; }
    QPushButton#btn_back {
        background-color: transparent; color: #95a5a6;
        border: none; font-size: 13px;
    }
    QPushButton#btn_back:hover { color: #7f8c8d; }
"""


class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RegisterWindow()
        self.ui.setupUi(self)
        self.centralWidget().setStyleSheet(STYLE)
        for f in [self.ui.input_nom, self.ui.input_email,
                  self.ui.input_mdp, self.ui.input_confirm]:
            f.setStyleSheet(FIELD)
            f.setFocusPolicy(Qt.StrongFocus)
        self.center()
        self.ui.btn_register.clicked.connect(self.on_register)
        self.ui.btn_goto_login.clicked.connect(self.on_goto_login)
        self.ui.btn_back.clicked.connect(self.on_back)

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(self.screen().availableGeometry().center())
        self.move(qr.topLeft())

    def on_register(self):
        nom     = self.ui.input_nom.text().strip()
        email   = self.ui.input_email.text().strip()
        mdp     = self.ui.input_mdp.text().strip()
        confirm = self.ui.input_confirm.text().strip()

        if not nom or not email or not mdp or not confirm:
            self.ui.label_error.setText("Veuillez remplir tous les champs.")
            return
        if mdp != confirm:
            self.ui.label_error.setText("Les mots de passe ne correspondent pas.")
            return
        if len(mdp) < 6:
            self.ui.label_error.setText("Le mot de passe doit contenir au moins 6 caracteres.")
            return

        res = inscrire_utilisateur(nom, email, mdp)
        if res["succes"]:
            self.ui.label_error.setText("")
            self.on_goto_login()
        else:
            self.ui.label_error.setText(res["erreur"])

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