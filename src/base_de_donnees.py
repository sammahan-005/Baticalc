# src/analyseurs/parseurIfc.py
import sys
import os
from src.configuration import DB_PATH
import sqlite3

# Allow imports from src/ when running standalone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analyseurs import analyseurIfc, walls, foundations, column, roof


def parseur(chemin_fichier: str) -> dict:
    """
    Analyse complète d'un fichier IFC.
    Retourne un dictionnaire avec tous les éléments extraits.
    """
    model = analyseurIfc.analyseur_fichier_ifc(chemin_fichier)
    if not model:
        return {"erreur": "Impossible d'ouvrir le fichier IFC."}

    resultats = {
        "murs":        [],
        "fondations":  [],
        "poteaux":     [],
        "toitures":    [],
        "erreurs":     []
    }

    try:
        resultats["murs"] = walls.parse_walls(model)
    except Exception as e:
        resultats["erreurs"].append(f"Murs: {e}")

    try:
        resultats["fondations"] = foundations.parse_foundations(model)
    except Exception as e:
        resultats["erreurs"].append(f"Fondations: {e}")

    try:
        resultats["poteaux"] = column.parse_columns(model)
    except Exception as e:
        resultats["erreurs"].append(f"Poteaux: {e}")

    try:
        resultats["toitures"] = roof.parse_roofs(model)
    except Exception as e:
        resultats["erreurs"].append(f"Toitures: {e}")

    # --- BLOC D’INSERTION EN BASE SQLITE (AJOUTÉ, SANS MODIFIER LE CODE AU-DESSUS) ---
    try:
     

        
        db_path = "batiment.db"

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        for mur in resultats["murs"]:
            cur.execute(
                """
                INSERT INTO murs (guid, nom_instance, type_ifc, surface, volume, hauteur)
                VALUES (:guid, :nom_instance, :type_ifc, :surface, :volume, :hauteur)
                """,
                mur,
            )


        for f in resultats["fondations"]:
            cur.execute(
                """
                INSERT INTO fondations (guid, nom_instance, type_ifc, volume, surface_base, perimetre, hauteur)
                VALUES (:guid, :nom_instance, :type_ifc, :volume, :surface_base, :perimetre, :hauteur)
                """,
                f,
            )

  
        for p in resultats["poteaux"]:
            cur.execute(
                """
                INSERT INTO poteaux (guid, nom, etage, materiau, hauteur, surface_section, volume_net, poids_estime_kg)
                VALUES (:guid, :nom, :etage, :materiau, :hauteur, :surface_section, :volume_net, :poids_estime_kg)
                """,
                p,
            )

        
        for t in resultats["toitures"]:
            cur.execute(
                """
                INSERT INTO toitures (id, guid, nom, type_objet, etage, surface_horizontale, surface_reelle, pente_moyenne)
                VALUES (:id, :guid, :nom, :type_objet, :etage, :surface_horizontale, :surface_reelle, :pente_moyenne)
                """,
                t,
            )

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        # On logge juste l'erreur d'insert, sans casser l’analyse
        resultats["erreurs"].append(f"BDD: {e}")


    return resultats
