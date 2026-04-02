# src/base_de_donnees.py
import sqlite3
import os
from src.configuration import DB_PATH


# ─────────────────────────────────────────────
#  Connexion
# ─────────────────────────────────────────────

def get_connection():
    """Retourne une connexion à la base SQLite."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ─────────────────────────────────────────────
#  Initialisation de toutes les tables
# ─────────────────────────────────────────────

def init_db():
    """Crée toutes les tables si elles n'existent pas encore."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""

        -- ── 1. UTILISATEURS ──────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            nom          TEXT    NOT NULL,
            email        TEXT    NOT NULL UNIQUE,
            mot_de_passe TEXT    NOT NULL,
            cree_le      TEXT    DEFAULT (datetime('now'))
        );

        -- ── 2. PROJETS ────────────────────────────────────────────────
        CREATE TABLE IF NOT EXISTS projets (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur_id INTEGER NOT NULL,
            nom            TEXT    NOT NULL,
            chemin_ifc     TEXT,
            statut         TEXT    DEFAULT 'en_attente',
            cree_le        TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
        );

        -- ── 3. MURS  (sorties réelles de walls.py) ───────────────────
        --  Champs réels : guid, nom_instance, type_ifc, nom_technique, surface, volume, hauteur
        CREATE TABLE IF NOT EXISTS murs (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            projet_id     INTEGER NOT NULL,
            guid          TEXT,
            nom_instance  TEXT,
            type_ifc      TEXT,
            nom_technique TEXT,
            surface       REAL    DEFAULT 0,
            volume        REAL    DEFAULT 0,
            hauteur       REAL    DEFAULT 0,
            FOREIGN KEY (projet_id) REFERENCES projets(id)
        );

        -- ── 4. FONDATIONS  (sorties réelles de foundations.py) ───────
        --  Champs réels : guid, nom_instance, type_ifc, volume, surface_base, perimetre, hauteur
        --  (surface_coffrage_lateral calculé = perimetre * hauteur)
        CREATE TABLE IF NOT EXISTS fondations (
            id                      INTEGER PRIMARY KEY AUTOINCREMENT,
            projet_id               INTEGER NOT NULL,
            guid                    TEXT,
            nom_instance            TEXT,
            type_ifc                TEXT,
            volume                  REAL    DEFAULT 0,
            surface_base            REAL    DEFAULT 0,
            perimetre               REAL    DEFAULT 0,
            hauteur                 REAL    DEFAULT 0,
            surface_coffrage_lateral REAL   DEFAULT 0,
            FOREIGN KEY (projet_id) REFERENCES projets(id)
        );

        -- ── 5. POTEAUX  (sorties réelles de column.py) ───────────────
        --  Champs réels : guid, nom, etage, materiau, hauteur, surface_section, volume_net
        --  (poids_estime_kg calculé si besoin)
        CREATE TABLE IF NOT EXISTS poteaux (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            projet_id        INTEGER NOT NULL,
            guid             TEXT,
            nom              TEXT,
            etage            TEXT,
            materiau         TEXT,
            hauteur          REAL    DEFAULT 0,
            surface_section  REAL    DEFAULT 0,
            volume_net       REAL    DEFAULT 0,
            poids_estime_kg  REAL    DEFAULT 0,
            FOREIGN KEY (projet_id) REFERENCES projets(id)
        );

        -- ── 6. TOITURES  (sorties réelles de roof.py) ────────────────
        --  Champs réels : guid, nom_instance, type_ifc, etage, surface_horizontale, surface_reelle, pente_moyenne
        CREATE TABLE IF NOT EXISTS toitures (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            projet_id           INTEGER NOT NULL,
            guid                TEXT,
            nom_instance        TEXT,
            type_ifc            TEXT,
            etage               TEXT,
            surface_horizontale REAL    DEFAULT 0,
            surface_reelle      REAL    DEFAULT 0,
            pente_moyenne       REAL    DEFAULT 0,
            FOREIGN KEY (projet_id) REFERENCES projets(id)
        );

        -- ── 7. DEVIS  (un devis par projet) ──────────────────────────
        CREATE TABLE IF NOT EXISTS devis (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            projet_id      INTEGER NOT NULL UNIQUE,
            date_creation  TEXT    DEFAULT (datetime('now')),
            montant_total  REAL    DEFAULT 0,
            FOREIGN KEY (projet_id) REFERENCES projets(id)
        );

        -- ── 8. LIGNES DE DEVIS  (détail matériau par matériau) ───────
        CREATE TABLE IF NOT EXISTS lignes_devis (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            devis_id       INTEGER NOT NULL,
            materiau       TEXT    NOT NULL,
            quantite       REAL    DEFAULT 0,
            unite          TEXT,
            prix_unitaire  REAL    DEFAULT 0,
            prix_total     REAL    DEFAULT 0,
            FOREIGN KEY (devis_id) REFERENCES devis(id)
        );

        -- ── 9. PRIX UNITAIRES  (table de référence des prix) ─────────
        --  Pré-remplie avec les matériaux standards du marché camerounais
        CREATE TABLE IF NOT EXISTS prix_unitaires (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            materiau  TEXT    NOT NULL UNIQUE,
            prix      REAL    NOT NULL,
            unite     TEXT    NOT NULL
        );

    """)
    conn.commit()
    conn.close()

    # Insérer les prix unitaires de référence si la table est vide
    _seed_prix_unitaires()


def _seed_prix_unitaires():
    """Insère les prix de référence (marché Yaoundé 2025) si absents."""
    conn = get_connection()
    cursor = conn.cursor()

    prix_ref = [
        # (materiau, prix, unite)
        ("Sacs ciment 50kg",         4500,    "sac"),
        ("Sable (m3)",               25000,   "m3"),
        ("Gravier (m3)",             30000,   "m3"),
        ("Sable fin (m3)",           25000,   "m3"),
        ("Barres HA06 (6m)",         1200,    "barre"),
        ("Barres HA08 (12m)",        3000,    "barre"),
        ("Barres HA10 (12m)",        4200,    "barre"),
        ("Barres HA12 (12m)",        5500,    "barre"),
        ("Parpaings 20x20x40",       350,     "parpaing"),
        ("Bac acier / couverture",   8000,    "m2"),
        ("Bois charpente (m3)",      180000,  "m3"),
        ("Clous / visserie (kg)",    1500,    "kg"),
    ]

    for materiau, prix, unite in prix_ref:
        cursor.execute("""
            INSERT OR IGNORE INTO prix_unitaires (materiau, prix, unite)
            VALUES (?, ?, ?)
        """, (materiau, prix, unite))

    conn.commit()
    conn.close()


# ─────────────────────────────────────────────
#  UTILISATEURS
# ─────────────────────────────────────────────

def inscrire_utilisateur(nom: str, email: str, mot_de_passe_hash: str) -> dict:
    """Insère un nouvel utilisateur. Retourne {succes, utilisateur} ou {succes, erreur}."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO utilisateurs (nom, email, mot_de_passe) VALUES (?, ?, ?)",
            (nom, email, mot_de_passe_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {"succes": True, "utilisateur": {"id": user_id, "nom": nom, "email": email}}
    except sqlite3.IntegrityError:
        return {"succes": False, "erreur": "Cet email est déjà utilisé."}
    except Exception as e:
        return {"succes": False, "erreur": str(e)}


def get_utilisateur_par_email(email: str):
    """Retourne la ligne utilisateur correspondant à l'email, ou None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    return row


# ─────────────────────────────────────────────
#  PROJETS
# ─────────────────────────────────────────────

def creer_projet(utilisateur_id: int, nom: str, chemin_ifc: str) -> dict:
    """Crée un nouveau projet et retourne son id."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO projets (utilisateur_id, nom, chemin_ifc, statut) VALUES (?, ?, ?, 'en_cours')",
            (utilisateur_id, nom, chemin_ifc)
        )
        conn.commit()
        projet_id = cursor.lastrowid
        conn.close()
        return {"succes": True, "projet_id": projet_id}
    except Exception as e:
        return {"succes": False, "erreur": str(e)}




def get_projets_utilisateur(utilisateur_id: int) -> list:
    """Retourne tous les projets d'un utilisateur, du plus récent au plus ancien."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM projets WHERE utilisateur_id = ? ORDER BY cree_le DESC",
        (utilisateur_id,)
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def mettre_a_jour_statut_projet(projet_id: int, statut: str):
    """Met à jour le statut d'un projet ('en_cours', 'termine', 'erreur')."""
    conn = get_connection()
    conn.execute(
        "UPDATE projets SET statut = ? WHERE id = ?", (statut, projet_id)
    )
    conn.commit()
    conn.close()




# ─────────────────────────────────────────────
#  SAUVEGARDE DES RÉSULTATS IFC
# ─────────────────────────────────────────────

def sauvegarder_murs(projet_id: int, murs: list):
    """Insère la liste des murs extraits du fichier IFC."""
    conn = get_connection()
    cursor = conn.cursor()
    for m in murs:
        cursor.execute("""
            INSERT INTO murs
                (projet_id, guid, nom_instance, type_ifc, nom_technique, surface, volume, hauteur)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            projet_id,
            m.get("guid", ""),
            m.get("nom_instance", ""),
            m.get("type_ifc", ""),
            m.get("nom_technique", ""),  # nouveau champ
            m.get("surface", 0),
            m.get("volume", 0),
            m.get("hauteur", 0),
        ))
    conn.commit()
    conn.close()


def sauvegarder_fondations(projet_id: int, fondations: list):
    """Insère la liste des fondations extraites du fichier IFC."""
    conn = get_connection()
    cursor = conn.cursor()
    for f in fondations:
        perimetre = f.get("perimetre", 0)
        hauteur   = f.get("hauteur", 0)
        coffrage  = perimetre * hauteur
        cursor.execute("""
            INSERT INTO fondations
                (projet_id, guid, nom_instance, type_ifc,
                 volume, surface_base, perimetre, hauteur, surface_coffrage_lateral)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            projet_id,
            f.get("guid", ""),
            f.get("nom_instance", ""),
            f.get("type_ifc", ""),
            f.get("volume", 0),
            f.get("surface_base", 0),
            perimetre,
            hauteur,
            coffrage,
        ))
    conn.commit()
    conn.close()


def sauvegarder_poteaux(projet_id: int, poteaux: list):
    """Insère la liste des poteaux extraits du fichier IFC."""
    conn = get_connection()
    cursor = conn.cursor()
    for p in poteaux:
        cursor.execute("""
            INSERT INTO poteaux
                (projet_id, guid, nom, etage, materiau,
                 hauteur, surface_section, volume_net, poids_estime_kg)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            projet_id,
            p.get("guid", ""),
            p.get("nom", ""),
            p.get("etage", ""),
            p.get("materiau", ""),
            p.get("hauteur", 0),
            p.get("surface_section", 0),
            p.get("volume_net", 0),
            p.get("poids_estime_kg", 0),  # calculé si besoin
        ))
    conn.commit()
    conn.close()


def sauvegarder_toitures(projet_id: int, toitures: list):
    """Insère la liste des toitures extraites du fichier IFC."""
    conn = get_connection()
    cursor = conn.cursor()
    for t in toitures:
        cursor.execute("""
            INSERT INTO toitures
                (projet_id, guid, nom_instance, type_ifc, etage,
                 surface_horizontale, surface_reelle, pente_moyenne)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            projet_id,
            t.get("guid", ""),
            t.get("nom_instance", ""),  # changé de 'nom'
            t.get("type_ifc", ""),      # changé de 'type_objet'
            t.get("etage", ""),
            t.get("surface_horizontale", 0),
            t.get("surface_reelle", 0),
            t.get("pente_moyenne", 0),
        ))
    conn.commit()
    conn.close()


def sauvegarder_resultats_ifc(projet_id: int, rapport: dict):
    """
    Point d'entrée unique : sauvegarde tous les éléments IFC
    d'un rapport dans leurs tables respectives.
    Appelé depuis results_handler.py après l'analyse.
    """
    sauvegarder_murs(projet_id,       rapport.get("murs", []))
    sauvegarder_fondations(projet_id, rapport.get("fondations", []))
    sauvegarder_poteaux(projet_id,    rapport.get("poteaux", []))
    sauvegarder_toitures(projet_id,   rapport.get("toitures", []))
    mettre_a_jour_statut_projet(projet_id, "termine")


# ─────────────────────────────────────────────
#  LECTURE DES RÉSULTATS IFC
# ─────────────────────────────────────────────

def get_murs(projet_id: int) -> list:
    conn = get_connection()
    rows = [dict(r) for r in conn.execute(
        "SELECT * FROM murs WHERE projet_id = ?", (projet_id,)
    ).fetchall()]
    conn.close()
    return rows


def get_fondations(projet_id: int) -> list:
    conn = get_connection()
    rows = [dict(r) for r in conn.execute(
        "SELECT * FROM fondations WHERE projet_id = ?", (projet_id,)
    ).fetchall()]
    conn.close()
    return rows


def get_poteaux(projet_id: int) -> list:
    conn = get_connection()
    rows = [dict(r) for r in conn.execute(
        "SELECT * FROM poteaux WHERE projet_id = ?", (projet_id,)
    ).fetchall()]
    conn.close()
    return rows


def get_toitures(projet_id: int) -> list:
    conn = get_connection()
    rows = [dict(r) for r in conn.execute(
        "SELECT * FROM toitures WHERE projet_id = ?", (projet_id,)
    ).fetchall()]
    conn.close()
    return rows


# ─────────────────────────────────────────────
#  DEVIS
# ─────────────────────────────────────────────

def sauvegarder_devis(projet_id: int, lignes: list) -> int:
    """
    Crée ou remplace le devis d'un projet.
    lignes : liste de dicts {materiau, quantite, unite, prix_unitaire, prix_total}
    Retourne l'id du devis créé.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Supprimer l'ancien devis s'il existe (remplacement)
    cursor.execute(
        "DELETE FROM lignes_devis WHERE devis_id IN "
        "(SELECT id FROM devis WHERE projet_id = ?)", (projet_id,)
    )
    cursor.execute("DELETE FROM devis WHERE projet_id = ?", (projet_id,))

    montant_total = sum(l.get("prix_total", 0) for l in lignes)

    cursor.execute(
        "INSERT INTO devis (projet_id, montant_total) VALUES (?, ?)",
        (projet_id, montant_total)
    )
    devis_id = cursor.lastrowid

    for l in lignes:
        cursor.execute("""
            INSERT INTO lignes_devis
                (devis_id, materiau, quantite, unite, prix_unitaire, prix_total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            devis_id,
            l.get("materiau", ""),
            l.get("quantite", 0),
            l.get("unite", ""),
            l.get("prix_unitaire", 0),
            l.get("prix_total", 0),
        ))

    conn.commit()
    conn.close()
    return devis_id


def get_devis(projet_id: int) -> dict:
    """
    Retourne le devis complet d'un projet :
    { devis: {...}, lignes: [...] }
    """
    conn = get_connection()
    devis_row = conn.execute(
        "SELECT * FROM devis WHERE projet_id = ?", (projet_id,)
    ).fetchone()

    if not devis_row:
        conn.close()
        return None

    devis_id = devis_row["id"]
    lignes = [dict(r) for r in conn.execute(
        "SELECT * FROM lignes_devis WHERE devis_id = ?", (devis_id,)
    ).fetchall()]

    conn.close()
    return {"devis": dict(devis_row), "lignes": lignes}


# ─────────────────────────────────────────────
#  PRIX UNITAIRES
# ─────────────────────────────────────────────

def get_tous_prix_unitaires() -> list:
    """Retourne tous les prix de la table de référence."""
    conn = get_connection()
    rows = [dict(r) for r in conn.execute(
        "SELECT * FROM prix_unitaires ORDER BY materiau"
    ).fetchall()]
    conn.close()
    return rows


def get_prix_unitaire(materiau: str) -> float:
    """Retourne le prix unitaire d'un matériau, ou 0 si inconnu."""
    conn = get_connection()
    row = conn.execute(
        "SELECT prix FROM prix_unitaires WHERE materiau = ?", (materiau,)
    ).fetchone()
    conn.close()
    return row["prix"] if row else 0.0


def mettre_a_jour_prix(materiau: str, nouveau_prix: float):
    """Met à jour le prix d'un matériau dans la table de référence."""
    conn = get_connection()
    conn.execute(
        "UPDATE prix_unitaires SET prix = ? WHERE materiau = ?",
        (nouveau_prix, materiau)
    )
    conn.commit()
    conn.close()