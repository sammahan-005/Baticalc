# src/ui_handlers/login_handler.py
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                QPushButton, QLabel, QLineEdit, QGraphicsOpacityEffect)
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QBrush, QPen, QPolygonF
from PySide6.QtCore import QPointF

STYLE = """
QMainWindow, QWidget {
    background-color: #0D1117;
}
QWidget#panel {
    background: #13191F;
    border-right: 1px solid rgba(255,255,255,0.06);
}
QWidget#form_card {
    background: transparent;
}
QLabel#brand {
    color: #F5C842;
    font-family: 'Georgia';
    font-size: 32px;
    font-weight: bold;
    letter-spacing: 6px;
}
QLabel#form_title {
    color: #FFFFFF;
    font-size: 22px;
    font-weight: bold;
    font-family: 'Georgia';
}
QLabel#form_sub {
    color: rgba(255,255,255,0.4);
    font-size: 13px;
}
QLabel#field_label {
    color: rgba(255,255,255,0.55);
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: bold;
}
QLineEdit {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    color: #FFFFFF;
    font-size: 14px;
    padding: 14px 18px;
    selection-background-color: #F5C842;
    selection-color: #0D1117;
}
QLineEdit:focus {
    border: 1.5px solid #F5C842;
    background: rgba(245,200,66,0.04);
}
QLineEdit::placeholder {
    color: rgba(255,255,255,0.2);
}
QPushButton#btn_main {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #F5C842, stop:1 #E8A020);
    color: #0D1117;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 1px;
    min-height: 52px;
}
QPushButton#btn_main:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #FFD55A, stop:1 #F0B030);
}
QPushButton#btn_main:pressed { background: #D4A010; }
QPushButton#btn_secondary {
    background: transparent;
    color: rgba(255,255,255,0.6);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    font-size: 13px;
    min-height: 44px;
}
QPushButton#btn_secondary:hover {
    background: rgba(255,255,255,0.05);
    color: #FFFFFF;
    border-color: rgba(255,255,255,0.25);
}
QPushButton#btn_back {
    background: transparent;
    color: rgba(255,255,255,0.3);
    border: none;
    font-size: 12px;
    letter-spacing: 1px;
    min-height: 32px;
    text-align: left;
}
QPushButton#btn_back:hover { color: rgba(255,255,255,0.7); }
QLabel#error_lbl {
    color: #FF6B6B;
    font-size: 12px;
    background: rgba(255,107,107,0.1);
    border: 1px solid rgba(255,107,107,0.25);
    border-radius: 8px;
    padding: 8px 14px;
}
QLabel#panel_quote {
    color: rgba(255,255,255,0.25);
    font-size: 12px;
    font-style: italic;
    line-height: 1.8;
}
"""


class SidePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("panel")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # grid
        pen = QPen(QColor(255, 255, 255, 6))
        painter.setPen(pen)
        for x in range(0, self.width(), 35):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), 35):
            painter.drawLine(0, y, self.width(), y)
        # gold triangle
        painter.setBrush(QBrush(QColor(245, 200, 66, 20)))
        painter.setPen(Qt.NoPen)
        tri = QPolygonF([QPointF(0, self.height()),
                          QPointF(self.width(), self.height()),
                          QPointF(0, self.height()-200)])
        painter.drawPolygon(tri)


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BATICALC — Connexion")
        self.resize(860, 580)
        self.setStyleSheet(STYLE)
        self._build_ui()
        self.center()
        self._animate_in()

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(self.screen().availableGeometry().center())
        self.move(qr.topLeft())

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main = QHBoxLayout(central)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # ── LEFT PANEL ────────────────────────────────
        panel = SidePanel()
        panel.setFixedWidth(300)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(36, 48, 36, 48)

        brand = QLabel("BATI\nCALC")
        brand.setObjectName("brand")
        panel_layout.addWidget(brand)

        panel_layout.addSpacing(16)
        accent = QLabel()
        accent.setFixedSize(40, 3)
        accent.setStyleSheet("background: #F5C842; border-radius: 2px;")
        panel_layout.addWidget(accent)

        panel_layout.addSpacing(24)
        quote = QLabel("Analysez votre maquette\nIFC et générez votre\ndevis en quelques\nsecondes.")
        quote.setObjectName("panel_quote")
        panel_layout.addWidget(quote)

        panel_layout.addStretch()

        # feature chips
        for feat in ["Murs", "Fondations", "Poteaux", "Toitures"]:
            chip = QLabel(f"  ✦  {feat}")
            chip.setStyleSheet("""
                color: rgba(245,200,66,0.6);
                font-size: 11px;
                letter-spacing: 1px;
                padding: 6px 0px;
            """)
            panel_layout.addWidget(chip)

        panel_layout.addSpacing(20)
        main.addWidget(panel)

        # ── RIGHT FORM ────────────────────────────────
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(60, 50, 60, 50)
        right_layout.setSpacing(0)

        # Back button
        self.btn_back = QPushButton("← Retour")
        self.btn_back.setObjectName("btn_back")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        right_layout.addWidget(self.btn_back, alignment=Qt.AlignLeft)

        right_layout.addStretch()

        title = QLabel("Connexion")
        title.setObjectName("form_title")
        right_layout.addWidget(title)

        sub = QLabel("Entrez vos identifiants pour accéder à votre espace")
        sub.setObjectName("form_sub")
        sub.setWordWrap(True)
        right_layout.addSpacing(8)
        right_layout.addWidget(sub)

        right_layout.addSpacing(36)

        # Email field
        lbl_email = QLabel("ADRESSE EMAIL")
        lbl_email.setObjectName("field_label")
        right_layout.addWidget(lbl_email)
        right_layout.addSpacing(8)
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("exemple@email.com")
        right_layout.addWidget(self.input_email)

        right_layout.addSpacing(20)

        # Password field
        lbl_pwd = QLabel("MOT DE PASSE")
        lbl_pwd.setObjectName("field_label")
        right_layout.addWidget(lbl_pwd)
        right_layout.addSpacing(8)
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("••••••••")
        self.input_password.setEchoMode(QLineEdit.Password)
        right_layout.addWidget(self.input_password)

        right_layout.addSpacing(16)

        # Error label (hidden by default)
        self.label_error = QLabel("")
        self.label_error.setObjectName("error_lbl")
        self.label_error.setWordWrap(True)
        self.label_error.hide()
        right_layout.addWidget(self.label_error)

        right_layout.addSpacing(28)

        # Main button
        self.btn_login = QPushButton("Se connecter")
        self.btn_login.setObjectName("btn_main")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        right_layout.addWidget(self.btn_login)

        right_layout.addSpacing(14)

        self.btn_goto_register = QPushButton("Pas encore de compte ? Créer un compte")
        self.btn_goto_register.setObjectName("btn_secondary")
        self.btn_goto_register.setCursor(Qt.PointingHandCursor)
        right_layout.addWidget(self.btn_goto_register)

        right_layout.addStretch()

        main.addWidget(right)

        # Connect
        self.btn_login.clicked.connect(self.on_login)
        self.btn_goto_register.clicked.connect(self.on_goto_register)
        self.btn_back.clicked.connect(self.on_back)
        self.input_password.returnPressed.connect(self.on_login)
        self.input_email.returnPressed.connect(lambda: self.input_password.setFocus())

    def _animate_in(self):
        self.eff = QGraphicsOpacityEffect(self.centralWidget())
        self.centralWidget().setGraphicsEffect(self.eff)
        self.anim = QPropertyAnimation(self.eff, b"opacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        QTimer.singleShot(50, self.anim.start)

    def _show_error(self, msg):
        self.label_error.setText(msg)
        self.label_error.show()

    def on_login(self):
        email = self.input_email.text().strip()
        pwd   = self.input_password.text().strip()
        if not email or not pwd:
            self._show_error("Veuillez remplir tous les champs.")
            return
        from src.authentification import connecter_utilisateur
        res = connecter_utilisateur(email, pwd)
        if res["succes"]:
            self.label_error.hide()
            from src.ui_handlers.dashboard_handler import DashboardWindow
            self.dashboard = DashboardWindow(utilisateur=res["utilisateur"])
            self.dashboard.show()
            self.close()
        else:
            self._show_error(res["erreur"])

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
