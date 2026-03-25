# src/analyseurs/parseurIfc.py
import sys
import os

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

    return resultats