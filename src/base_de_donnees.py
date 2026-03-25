# src/base_de_donnees.py
import sqlite3
import os
from src.configuration import DB_PATH


def get_connection():
    """Return a connection to the SQLite database."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nom         TEXT    NOT NULL,
            email       TEXT    NOT NULL UNIQUE,
            mot_de_passe TEXT   NOT NULL,
            cree_le     TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS projets (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur_id INTEGER NOT NULL,
            nom         TEXT    NOT NULL,
            chemin_ifc  TEXT,
            statut      TEXT    DEFAULT 'en_attente',
            cree_le     TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
        );

        CREATE TABLE IF NOT EXISTS resultats (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            projet_id   INTEGER NOT NULL,
            categorie   TEXT,
            designation TEXT,
            quantite    REAL,
            unite       TEXT,
            cree_le     TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (projet_id) REFERENCES projets(id)
        );
    """)
    conn.commit()
    conn.close()