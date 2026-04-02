# src/configuration.py
import os

# Project root = parent of src/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SQLite database path
DB_PATH = os.path.join(BASE_DIR, "data", "baticalc.db")

# PDF reports output folder
REPORTS_DIR = os.path.join(BASE_DIR, "data", "reports")

# App info
APP_NAME    = "BATICALC"
APP_VERSION = "1.0.0"
APP_SLOGAN  = "Calculateur BIM pour Gros Oeuvre"