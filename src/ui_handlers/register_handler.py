# src/ui_handlers/register_handler.py
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                QPushButton, QLabel, QLineEdit, QGraphicsOpacityEffect)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QPolygonF
from PySide6.QtCore import QPointF

STYLE = """
QMainWindow, QWidget {
    background-color: #0D1117;
}
QWidget#panel {
    background: #13191F;
    border-right: 1px solid rgba(255,255,255,0.06);
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
    padding: 12px 18px;
    selection-background-color: #2ECC71;
    selection-color: #0D1117;
}
QLineEdit:focus {
    border: 1.5px solid #2ECC71;
    background: rgba(46,204,113,0.04);
}
QPushButton#btn_main {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #2ECC71, stop:1 #27AE60);
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 1px;
    min-height: 52px;
}
QPushButton#btn_main:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #3DD880, stop:1 #2EBD6A);
}
QPushButton#btn_main:pressed { background: #219A52; }
QPushButton#btn_secondary {
    background: transparent;
    color: rgba(255,255,255,0.55);
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
QLabel#success_lbl {
    color: #2ECC71;
    font-size: 12px;
    background: rgba(46,204,113,0.1);
    border: 1px solid rgba(46,204,113,0.25);
    border-radius: 8px;
    padding: 8px 14px;
}
QLabel#panel_quote {
    color: rgba(255,255,255,0.25);
    font-size: 12px;
    font-style: italic;
}
"""


class SidePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("panel")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(255, 255, 255, 6))
        painter.setPen(pen)
        for x in range(0, self.width(), 35):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), 35):
            painter.drawLine(0, y, self.width(), y)
        painter.setBrush(QBrush(QColor(46, 204, 113, 18)))
        painter.setPen(Qt.NoPen)
        tri = QPolygonF([QPointF(0, self.height()),
                          QPointF(self.width(), self.height()),
                          QPointF(0, self.height()-220)])
        painter.drawPolygon(tri)


class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BATICALC — Inscription")
        self.resize(860, 640)
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
        pv = QVBoxLayout(panel)
        pv.setContentsMargins(36, 48, 36, 48)

        brand = QLabel("BATI\nCALC")
        brand.setObjectName("brand")
        pv.addWidget(brand)

        pv.addSpacing(16)
        accent = QLabel()
        accent.setFixedSize(40, 3)
        accent.setStyleSheet("background: #2ECC71; border-radius: 2px;")
        pv.addWidget(accent)

        pv.addSpacing(24)
        quote = QLabel("Créez votre compte\ngratuit et commencez\nà analyser vos\nfichiers IFC.")
        quote.setObjectName("panel_quote")
        pv.addWidget(quote)

        pv.addStretch()

        steps = [
            ("01", "Créer un compte"),
            ("02", "Importer un IFC"),
            ("03", "Obtenir le devis"),
        ]
        for num, step in steps:
            row = QHBoxLayout()
            n_lbl = QLabel(num)
            n_lbl.setStyleSheet("color: #2ECC71; font-size: 10px; font-weight: bold; min-width: 24px;")
            s_lbl = QLabel(step)
            s_lbl.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 11px;")
            row.addWidget(n_lbl)
            row.addWidget(s_lbl)
            row.addStretch()
            pv.addLayout(row)
            pv.addSpacing(8)

        pv.addSpacing(10)
        main.addWidget(panel)

        # ── RIGHT FORM ────────────────────────────────
        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setContentsMargins(56, 44, 56, 44)
        rv.setSpacing(0)

        self.btn_back = QPushButton("← Retour")
        self.btn_back.setObjectName("btn_back")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        rv.addWidget(self.btn_back, alignment=Qt.AlignLeft)

        rv.addSpacing(20)

        title = QLabel("Créer un compte")
        title.setObjectName("form_title")
        rv.addWidget(title)

        sub = QLabel("Remplissez le formulaire pour commencer gratuitement")
        sub.setObjectName("form_sub")
        rv.addSpacing(6)
        rv.addWidget(sub)

        rv.addSpacing(28)

        # Two-column row: nom
        def field(label_text, placeholder, echo=False):
            lbl = QLabel(label_text)
            lbl.setObjectName("field_label")
            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            if echo:
                inp.setEchoMode(QLineEdit.Password)
            return lbl, inp

        lbl_nom, self.input_nom = field("NOM COMPLET", "Jean Dupont")
        rv.addWidget(lbl_nom)
        rv.addSpacing(6)
        rv.addWidget(self.input_nom)

        rv.addSpacing(16)

        lbl_email, self.input_email = field("ADRESSE EMAIL", "exemple@email.com")
        rv.addWidget(lbl_email)
        rv.addSpacing(6)
        rv.addWidget(self.input_email)

        rv.addSpacing(16)

        # Two password fields side by side
        pwd_row = QHBoxLayout()
        pwd_row.setSpacing(16)

        pwd_left = QVBoxLayout()
        lbl_pwd, self.input_mdp = field("MOT DE PASSE", "••••••••", echo=True)
        pwd_left.addWidget(lbl_pwd)
        pwd_left.addSpacing(6)
        pwd_left.addWidget(self.input_mdp)
        pwd_row.addLayout(pwd_left)

        pwd_right = QVBoxLayout()
        lbl_conf, self.input_confirm = field("CONFIRMER", "••••••••", echo=True)
        pwd_right.addWidget(lbl_conf)
        pwd_right.addSpacing(6)
        pwd_right.addWidget(self.input_confirm)
        pwd_row.addLayout(pwd_right)

        rv.addLayout(pwd_row)

        rv.addSpacing(14)

        self.label_error = QLabel("")
        self.label_error.setObjectName("error_lbl")
        self.label_error.setWordWrap(True)
        self.label_error.hide()
        rv.addWidget(self.label_error)

        rv.addSpacing(24)

        self.btn_register = QPushButton("Créer mon compte")
        self.btn_register.setObjectName("btn_main")
        self.btn_register.setCursor(Qt.PointingHandCursor)
        rv.addWidget(self.btn_register)

        rv.addSpacing(12)

        self.btn_goto_login = QPushButton("Déjà un compte ? Se connecter")
        self.btn_goto_login.setObjectName("btn_secondary")
        self.btn_goto_login.setCursor(Qt.PointingHandCursor)
        rv.addWidget(self.btn_goto_login)

        rv.addStretch()

        main.addWidget(right)

        self.btn_register.clicked.connect(self.on_register)
        self.btn_goto_login.clicked.connect(self.on_goto_login)
        self.btn_back.clicked.connect(self.on_back)

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
        self.label_error.setObjectName("error_lbl")
        self.label_error.setStyleSheet("color: #FF6B6B; font-size: 12px; background: rgba(255,107,107,0.1); border: 1px solid rgba(255,107,107,0.25); border-radius: 8px; padding: 8px 14px;")
        self.label_error.setText(msg)
        self.label_error.show()

    def on_register(self):
        nom     = self.input_nom.text().strip()
        email   = self.input_email.text().strip()
        mdp     = self.input_mdp.text().strip()
        confirm = self.input_confirm.text().strip()
        if not nom or not email or not mdp or not confirm:
            self._show_error("Veuillez remplir tous les champs.")
            return
        if mdp != confirm:
            self._show_error("Les mots de passe ne correspondent pas.")
            return
        if len(mdp) < 6:
            self._show_error("Le mot de passe doit contenir au moins 6 caractères.")
            return
        from src.authentification import inscrire_utilisateur
        res = inscrire_utilisateur(nom, email, mdp)
        if res["succes"]:
            self.label_error.hide()
            self.on_goto_login()
        else:
            self._show_error(res["erreur"])

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
