# src/analyseurs/parseurIfc.py
import sys
import os
from src.configuration import DB_PATH
from src.analyseurs import analyseurIfc, walls, foundations, column, roof
from src.base_de_donnees import sauvegarder_murs, sauvegarder_fondations, sauvegarder_poteaux, sauvegarder_toitures
import session
from src.calculateur import calculateur



sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))




def parseur(chemin_fichier: str) -> dict:
    """
    Analyse complète d'un fichier IFC.
    Sauvegarde les résultats dans la base de données.
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
        sauvegarder_murs(session.projet_actuel["id"], resultats["murs"])

    except Exception as e:
        resultats["erreurs"].append(f"Murs: {e}")

    try:

        resultats["fondations"] = foundations.parse_foundations(model)
        sauvegarder_fondations(session.projet_actuel["id"], resultats["fondations"])
    
    except Exception as e:
        resultats["erreurs"].append(f"Fondations: {e}")

    try:

        resultats["poteaux"] = column.parse_columns(model)
        sauvegarder_poteaux(session.projet_actuel["id"], resultats["poteaux"])

    except Exception as e:
        resultats["erreurs"].append(f"Poteaux: {e}")

    try:

        resultats["toitures"] = roof.parse_roofs(model)
        sauvegarder_toitures(session.projet_actuel["id"], resultats["toitures"])

    except Exception as e:
        resultats["erreurs"].append(f"Toitures: {e}")

    

  


    return resultats
