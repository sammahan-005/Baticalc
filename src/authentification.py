# src/authentification.py
import hashlib
from src.base_de_donnees import get_connection


def _hacher_mot_de_passe(mot_de_passe: str) -> str:
    sel = "baticalc_2024"
    return hashlib.sha256(f"{sel}{mot_de_passe}".encode()).hexdigest()


def inscrire_utilisateur(nom: str, email: str, mot_de_passe: str) -> dict:
    """
    Inscrit un nouvel utilisateur.
    Retourne {"succes": True, "utilisateur": {...}}
         ou  {"succes": False, "erreur": "..."}
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id FROM utilisateurs WHERE email = ?", (email.lower(),)
        )
        if cursor.fetchone():
            return {"succes": False, "erreur": "Cet email est déjà utilisé."}

        hache = _hacher_mot_de_passe(mot_de_passe)
        cursor.execute(
            "INSERT INTO utilisateurs (nom, email, mot_de_passe) VALUES (?, ?, ?)",
            (nom, email.lower(), hache)
        )
        conn.commit()
        cursor.execute(
            "SELECT id, nom, email FROM utilisateurs WHERE email = ?",
            (email.lower(),)
        )
        utilisateur = dict(cursor.fetchone())
        return {"succes": True, "utilisateur": utilisateur}
    except Exception as e:
        return {"succes": False, "erreur": str(e)}
    finally:
        conn.close()


def connecter_utilisateur(email: str, mot_de_passe: str) -> dict:
    """
    Authentifie un utilisateur.
    Retourne {"succes": True, "utilisateur": {...}}
         ou  {"succes": False, "erreur": "..."}
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hache = _hacher_mot_de_passe(mot_de_passe)
        cursor.execute(
            "SELECT id, nom, email FROM utilisateurs "
            "WHERE email = ? AND mot_de_passe = ?",
            (email.lower(), hache)
        )
        row = cursor.fetchone()
        if row:
            return {"succes": True, "utilisateur": dict(row)}
        return {"succes": False, "erreur": "Email ou mot de passe incorrect."}
    except Exception as e:
        return {"succes": False, "erreur": str(e)}
    finally:
        conn.close()


# def get_projets_utilisateur(utilisateur_id: int) -> list:
#     """Retourne tous les projets d'un utilisateur."""
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(
#         "SELECT * FROM projets WHERE utilisateur_id = ? "
#         "ORDER BY cree_le DESC",
#         (utilisateur_id,)
#     )
#     rows = [dict(r) for r in cursor.fetchall()]
#     conn.close()
#     return rows


# def creer_projet(utilisateur_id: int, nom: str, chemin_ifc: str = None) -> dict:
#     """Crée un nouveau projet."""
#     conn = get_connection()
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO projets (utilisateur_id, nom, chemin_ifc, statut) "
#             "VALUES (?, ?, ?, 'en_attente')",
#             (utilisateur_id, nom, chemin_ifc)
#         )
#         conn.commit()
#         projet_id = cursor.lastrowid
#         cursor.execute("SELECT * FROM projets WHERE id = ?", (projet_id,))
#         return {"succes": True, "projet": dict(cursor.fetchone())}
#     except Exception as e:
#         return {"succes": False, "erreur": str(e)}
#     finally:
#         conn.close()