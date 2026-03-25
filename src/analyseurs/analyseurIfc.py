import ifcopenshell


def analyseur_fichier_ifc(chemin_fichier):
    """
    Retourne une liste de murs avec les données nécessaires au calcul de devis.
    """
    try:
        model = ifcopenshell.open(chemin_fichier)
        return model
    except Exception as e:
        print(f"Erreur d'ouverture : {e}")
        return 0

    



