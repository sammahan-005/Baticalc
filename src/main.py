# src/main.py
import sys
import os

# Make sure project root is always on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from src.base_de_donnees import init_db
from src.ui_handlers.welcome_handler import WelcomeWindow


if __name__ == "__main__":
    init_db()  # Create tables if they don't exist

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = WelcomeWindow()
    window.show()

    sys.exit(app.exec())