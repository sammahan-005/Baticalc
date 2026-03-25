import ifcopenshell
import ifcopenshell.util.element

def extraire_donnees_devis_toiture(element):
    """
    Extrait les données de surfaces, pentes et matériaux pour le devis d'une toiture.
    Compatible avec IfcRoof et IfcSlab (Type ROOF).
    """
    
    info = {
        "id": element.id(),
        "nom": element.Name or "Toiture sans nom",
        "type_objet": element.is_a(), # IfcRoof ou IfcSlab
        "etage": "",
        "surface_horizontale": 0, # Surface projetée au sol
        "surface_reelle": 0,      # Surface inclinée (développée)
        "pente_moyenne": 0,       # En degrés ou pourcentage
        "materiaux": []
    }

   
    container = ifcopenshell.util.element.get_container(element)
    if container:
        info["etage"] = container.Name

    # 3. Extraction des quantités (Qto_RoofBaseQuantities ou Qto_SlabBaseQuantities)
    psets = ifcopenshell.util.element.get_psets(element)
    
    # On cherche dans les sets de quantités standards
    qto_names = ["Qto_RoofBaseQuantities", "Qto_SlabBaseQuantities", "Pset_Revit_Dimensions"]
    for name in qto_names:
        if name in psets:
            qto = psets[name]
            # Surface projetée (vue de dessus)
            info["surface_horizontale"] = qto.get("GrossArea", qto.get("Area", 0))
            # Surface réelle (si inclinée)
            info["surface_reelle"] = qto.get("NetSurfaceArea", info["surface_horizontale"])
            break

    # 4. Extraction de la pente (Slope)
    # Souvent dans Pset_RoofCommon ou calculée via les propriétés de type
    common_set = psets.get("Pset_RoofCommon", psets.get("Pset_SlabCommon", {}))
    info["pente_moyenne"] = common_set.get("Slope", 0)

    # 5. Liste des composants / Matériaux
    # Pour une toiture, on peut avoir un complexe (Isolant + Étanchéité)
    material_assoc = ifcopenshell.util.element.get_material(element)
    if material_assoc:
        if hasattr(material_assoc, "Materials"): # Si c'est un IfcMaterialList
            info["materiaux"] = [m.Name for m in material_assoc.Materials]
        elif hasattr(material_assoc, "Name"):    # Si c'est un matériau unique
            info["materiaux"] = [material_assoc.Name]

    return info