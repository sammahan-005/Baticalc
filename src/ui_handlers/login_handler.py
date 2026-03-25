# src/ui_handlers/login_handler.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow
from generated.ui_login import Ui_LoginWindow
from src.authentification import connecter_utilisateur

FIELD = """
    QLineEdit {
        border: 2px solid #bdc3c7; border-radius: 5px;
        padding: 8px 12px; font-size: 14px;
        background-color: white; color: #2c3e50;
    }
    QLineEdit:focus { border: 2px solid #3498db; }
"""
STYLE = """
    QWidget { background-color: #f5f5f5; }
    QLabel#label_title    { color: #2c3e50; font-size: 36px; font-weight: bold; }
    QLabel#label_subtitle { color: #7f8c8d; font-size: 14px; }
    QLabel#label_email, QLabel#label_password { color: #34495e; font-size: 13px; font-weight: bold; }
    QLabel#label_error    { color: #e74c3c; font-size: 13px; }
    QLabel#label_sep      { color: #7f8c8d; font-size: 13px; }
    QPushButton#btn_login {
        background-color: #3498db; color: white; border: none;
        border-radius: 5px; font-size: 16px; font-weight: bold;
    }
    QPushButton#btn_login:hover { background-color: #2980b9; }
    QPushButton#btn_goto_register {
        background-color: white; color: #2ecc71;
        border: 2px solid #2ecc71; border-radius: 5px;
        font-size: 16px; font-weight: bold;
    }
    QPushButton#btn_goto_register:hover { background-color: #2ecc71; color: white; }
    QPushButton#btn_back {
        background-color: transparent; color: #95a5a6;
        border: none; font-size: 13px;
    }
    QPushButton#btn_back:hover { color: #7f8c8d; }
"""


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.centralWidget().setStyleSheet(STYLE)
        for f in [self.ui.input_email, self.ui.input_password]:
            f.setStyleSheet(FIELD)
            f.setFocusPolicy(Qt.StrongFocus)
        self.center()
        self.ui.btn_login.clicked.connect(self.on_login)
        self.ui.btn_goto_register.clicked.connect(self.on_goto_register)
        self.ui.btn_back.clicked.connect(self.on_back)

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(self.screen().availableGeometry().center())
        self.move(qr.topLeft())

    def on_login(self):
        email = self.ui.input_email.text().strip()
        mdp   = self.ui.input_password.text().strip()
        if not email or not mdp:
            self.ui.label_error.setText("Veuillez remplir tous les champs.")
            return
        res = connecter_utilisateur(email, mdp)
        if res["succes"]:
            self.ui.label_error.setText("")
            from src.ui_handlers.dashboard_handler import DashboardWindow
            self.dashboard = DashboardWindow(utilisateur=res["utilisateur"])
            self.dashboard.show()
            self.close()
        else:
            self.ui.label_error.setText(res["erreur"])

    def on_goto_register(self):
        from src.ui_handlers.register_handler import RegisterWindow
        self.register = RegisterWindow()
        self.register.show()
        self.close()

    def on_back(self):
        from src.ui_handlers.welcome_handler import WelcomeWindow
        self.welcome = WelcomeWindow()
        self.welcome.show()
        self.close()