import ifcopenshell
import ifcopenshell.util.element

def parse_columns(model):
    """
    Extrait les données nécessaires au métré et au devis d'un poteau IFC.
    """

    donnees_poteaux = []
    columns = model.by_type("IfcColumn")
    
    # Ajouter aussi les IfcColumnStandardCase (sous-classe de IfcColumn)
    columns.extend(model.by_type("IfcColumnStandardCase"))
    
    # Éliminer les doublons
    columns = list({col.id(): col for col in columns}.values())

    # --- DEBUT DE L'EXTRACTION POUR LE DEVIS ---
    for col in columns:
        # 1. Récupération des jeux de propriétés (quantités)
        psets = ifcopenshell.util.element.get_psets(col)
        qto = psets.get("Qto_ColumnBaseQuantities", {})

        # 2. Identification du niveau (Étage)
        container = ifcopenshell.util.element.get_container(col)
        nom_etage = container.Name if container else "Indéterminé"

        # 3. Récupération du matériau (pour le prix au m3)
        mat = ifcopenshell.util.element.get_material(col)
        nom_mat = mat.Name if mat and hasattr(mat, "Name") else "Béton standard"

        # 4. Construction du dictionnaire pour le devis
        info = {
            "guid": col.GlobalId,
            "nom": col.Name or "Poteau Sans Nom",
            "etage": nom_etage,
            "materiau": nom_mat,
            # Quantités clés pour le calcul financier
            "hauteur": round(qto.get("Length", 0), 2),        # Pour le coffrage linéaire
            "surface_section": round(qto.get("CrossSectionArea", 0), 3),
            "volume_net": round(qto.get("NetVolume", 0), 3),  # Pour la commande de béton
            "poids_estime_kg": round(qto.get("NetVolume", 0) * 2500, 0) # Base 2500kg/m3
        }

        donnees_poteaux.append(info)

    return donnees_poteaux