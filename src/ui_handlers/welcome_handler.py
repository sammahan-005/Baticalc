# src/ui_handlers/welcome_handler.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow
from generated.ui_welcome import Ui_WelcomeWindow

STYLE = """
    QWidget { background-color: #f5f5f5; }
    QLabel#label_title  { color: #2c3e50; font-size: 48px; font-weight: bold; }
    QLabel#label_subtitle { color: #7f8c8d; font-size: 16px; margin-bottom: 10px; }
    QLabel#label_desc   { color: #7f8c8d; font-size: 14px; padding: 20px; }
    QPushButton#btn_login {
        background-color: #3498db; color: white; border: none;
        border-radius: 5px; font-size: 16px; font-weight: bold;
    }
    QPushButton#btn_login:hover { background-color: #2980b9; }
    QPushButton#btn_register {
        background-color: #2ecc71; color: white; border: none;
        border-radius: 5px; font-size: 16px; font-weight: bold;
    }
    QPushButton#btn_register:hover { background-color: #27ae60; }
"""


class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WelcomeWindow()
        self.ui.setupUi(self)
        self.centralWidget().setStyleSheet(STYLE)
        self.center()
        self.ui.btn_login.clicked.connect(self.on_login)
        self.ui.btn_register.clicked.connect(self.on_register)

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(self.screen().availableGeometry().center())
        self.move(qr.topLeft())

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