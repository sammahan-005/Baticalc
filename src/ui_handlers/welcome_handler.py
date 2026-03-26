# src/ui_handlers/welcome_handler.py
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGraphicsOpacityEffect
from PySide6.QtGui import QFont, QLinearGradient, QPalette, QColor, QPainter, QBrush, QPen, QPolygonF
from PySide6.QtCore import QPointF
import math

STYLE = """
QMainWindow, QWidget#bg {
    background-color: #0D1117;
}
QWidget#card {
    background-color: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 24px;
}
QLabel#logo_text {
    color: #F5C842;
    font-family: 'Georgia';
    font-size: 56px;
    font-weight: bold;
    letter-spacing: 8px;
}
QLabel#tagline {
    color: rgba(255,255,255,0.5);
    font-family: 'Georgia';
    font-size: 13px;
    letter-spacing: 4px;
}
QLabel#desc {
    color: rgba(255,255,255,0.65);
    font-size: 14px;
    line-height: 1.8;
}
QLabel#divider {
    color: #F5C842;
    font-size: 11px;
    letter-spacing: 3px;
}
QPushButton#btn_login {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #F5C842, stop:1 #E8A020);
    color: #0D1117;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 1px;
    padding: 0px 40px;
    min-height: 52px;
    min-width: 200px;
}
QPushButton#btn_login:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #FFD55A, stop:1 #F0B030);
}
QPushButton#btn_login:pressed {
    background: #D4A010;
}
QPushButton#btn_register {
    background: transparent;
    color: #F5C842;
    border: 1.5px solid #F5C842;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
    letter-spacing: 1px;
    padding: 0px 40px;
    min-height: 52px;
    min-width: 200px;
}
QPushButton#btn_register:hover {
    background: rgba(245,200,66,0.1);
    border: 1.5px solid #FFD55A;
    color: #FFD55A;
}
QPushButton#btn_register:pressed {
    background: rgba(245,200,66,0.15);
}
QLabel#stat_num {
    color: #F5C842;
    font-size: 22px;
    font-weight: bold;
}
QLabel#stat_label {
    color: rgba(255,255,255,0.4);
    font-size: 10px;
    letter-spacing: 2px;
}
QWidget#stat_box {
    background: rgba(245,200,66,0.05);
    border: 1px solid rgba(245,200,66,0.15);
    border-radius: 12px;
}
"""


class GridBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Subtle grid
        pen = QPen(QColor(255, 255, 255, 8))
        pen.setWidth(1)
        painter.setPen(pen)
        spacing = 40
        for x in range(0, self.width(), spacing):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), spacing):
            painter.drawLine(0, y, self.width(), y)

        # Corner accent triangles
        gold = QColor(245, 200, 66, 30)
        painter.setBrush(QBrush(gold))
        painter.setPen(Qt.NoPen)
        tri1 = QPolygonF([QPointF(0,0), QPointF(180,0), QPointF(0,180)])
        painter.drawPolygon(tri1)
        tri2 = QPolygonF([QPointF(self.width(), self.height()),
                           QPointF(self.width()-180, self.height()),
                           QPointF(self.width(), self.height()-180)])
        painter.drawPolygon(tri2)

        # Glowing circles
        for cx, cy, r, alpha in [(650, 200, 200, 15), (100, 500, 150, 10)]:
            grad = QLinearGradient(cx-r, cy-r, cx+r, cy+r)
            grad.setColorAt(0, QColor(245, 200, 66, alpha))
            grad.setColorAt(1, QColor(245, 200, 66, 0))
            painter.setBrush(QBrush(grad))
            painter.drawEllipse(cx-r, cy-r, r*2, r*2)


class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BATICALC")
        self.resize(900, 620)
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
        central.setObjectName("bg")
        self.setCentralWidget(central)

        # Grid background
        self.grid = GridBackground(central)
        self.grid.setGeometry(0, 0, 900, 620)

        main = QHBoxLayout(central)
        main.setContentsMargins(60, 50, 60, 50)
        main.setSpacing(0)

        # ── LEFT: branding ──────────────────────────
        left = QVBoxLayout()
        left.setSpacing(0)

        logo = QLabel("BATICALC")
        logo.setObjectName("logo_text")
        left.addWidget(logo)

        tagline = QLabel("CALCULATEUR BIM — GROS OEUVRE")
        tagline.setObjectName("tagline")
        left.addSpacing(6)
        left.addWidget(tagline)

        # Gold accent line
        line = QLabel()
        line.setFixedSize(60, 3)
        line.setStyleSheet("background: #F5C842; border-radius: 2px;")
        left.addSpacing(24)
        left.addWidget(line)

        left.addSpacing(20)
        desc = QLabel("Importez un fichier IFC et obtenez\ninstantanément votre devis en\nmatériaux : ciment, fers, parpaings.")
        desc.setObjectName("desc")
        desc.setWordWrap(True)
        left.addWidget(desc)

        left.addSpacing(40)

        # Stats row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)
        for num, lbl in [("IFC", "FORMAT"), ("4", "ÉLÉMENTS"), ("PDF", "EXPORT")]:
            box = QWidget()
            box.setObjectName("stat_box")
            box.setFixedSize(90, 72)
            vb = QVBoxLayout(box)
            vb.setContentsMargins(0, 8, 0, 8)
            vb.setSpacing(2)
            n = QLabel(num)
            n.setObjectName("stat_num")
            n.setAlignment(Qt.AlignCenter)
            l = QLabel(lbl)
            l.setObjectName("stat_label")
            l.setAlignment(Qt.AlignCenter)
            vb.addWidget(n)
            vb.addWidget(l)
            stats_row.addWidget(box)
        stats_row.addStretch()
        left.addLayout(stats_row)

        left.addStretch()

        # Version badge
        ver = QLabel("VERSION 1.0  •  MARS 2026")
        ver.setStyleSheet("color: rgba(255,255,255,0.25); font-size: 10px; letter-spacing: 2px;")
        left.addWidget(ver)

        main.addLayout(left, 55)
        main.addSpacing(40)

        # ── RIGHT: card with buttons ─────────────────
        right_wrap = QVBoxLayout()
        right_wrap.addStretch()

        card = QWidget()
        card.setObjectName("card")
        card.setFixedWidth(340)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(36, 48, 36, 48)
        card_layout.setSpacing(0)

        welcome_lbl = QLabel("Bienvenue")
        welcome_lbl.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 26px; font-weight: bold; font-family: Georgia;")
        card_layout.addWidget(welcome_lbl)

        sub = QLabel("Connectez-vous ou créez\nun compte pour commencer.")
        sub.setStyleSheet("color: rgba(255,255,255,0.45); font-size: 13px; line-height: 1.6;")
        sub.setWordWrap(True)
        card_layout.addSpacing(10)
        card_layout.addWidget(sub)

        card_layout.addSpacing(36)

        self.btn_login = QPushButton("Se connecter")
        self.btn_login.setObjectName("btn_login")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.btn_login)

        card_layout.addSpacing(14)

        self.btn_register = QPushButton("Créer un compte")
        self.btn_register.setObjectName("btn_register")
        self.btn_register.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.btn_register)

        card_layout.addSpacing(32)

        # small note
        note = QLabel("Données 100% locales — aucun serveur")
        note.setStyleSheet("color: rgba(255,255,255,0.25); font-size: 11px; letter-spacing: 1px;")
        note.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(note)

        right_wrap.addWidget(card)
        right_wrap.addStretch()

        main.addLayout(right_wrap, 45)

        # Connect
        self.btn_login.clicked.connect(self.on_login)
        self.btn_register.clicked.connect(self.on_register)

        # Store card for animation
        self.card = card

    def _animate_in(self):
        self.effect = QGraphicsOpacityEffect(self.card)
        self.card.setGraphicsEffect(self.effect)
        self.anim = QPropertyAnimation(self.effect, b"opacity")
        self.anim.setDuration(700)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        QTimer.singleShot(100, self.anim.start)

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
