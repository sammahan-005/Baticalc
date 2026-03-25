import ifcopenshell
import ifcopenshell.util.element

def parse_foundations(model):
    donnees_fondations = []
    # On récupère les fondations (IfcFooting) et les radiers (souvent IfcSlab)
    foundations = model.by_type("IfcFooting")
    slabs = model.by_type("IfcSlab")

    # On fusionne les listes pour traiter tout ce qui touche au sol
    elements = foundations + [s for s in slabs if ifcopenshell.util.element.get_type(s) and 
                               ifcopenshell.util.element.get_type(s).PredefinedType == "BASESLAB"]

    for element in elements:
        # 1. Infos de base
        info = {
            "guid": element.GlobalId,
            "nom_instance": element.Name or "Fondation sans nom",
            "type_ifc": "NOTDEFINED",
            "nom_technique": "Inconnu",
            "materiau": "Béton Armé (par défaut)"
        }

        # 2. Analyse du Type (Semelle isolée, filante, etc.)
        element_type = ifcopenshell.util.element.get_type(element)
        if element_type:
            info["type_ifc"] = getattr(element_type, "PredefinedType", "NOTDEFINED")
            info["nom_technique"] = element_type.Name or "Type inconnu"

        # 3. Extraction des quantités (Pset_FootingCommon ou Qto_FootingBaseQuantities)
        psets = ifcopenshell.util.element.get_psets(element)
        qto = {**psets.get("BaseQuantities", {}), **psets.get("Qto_FootingBaseQuantities", {}), **psets.get("Qto_SlabBaseQuantities", {})}
        
        
        info["volume"] = qto.get("NetVolume", 0)
        info["surface_base"] = qto.get("GrossArea", qto.get("NetArea", 0)) # Emprise au sol
        info["perimetre"] = qto.get("Perimeter", 0) # Utile pour le coffrage latéral
        
        
        hauteur = qto.get("Height", 0)
        if hauteur == 0 and info["surface_base"] > 0:
            hauteur = info["volume"] / info["surface_base"]
        
        info["hauteur"] = hauteur
        info["surface_coffrage_lateral"] = info["perimetre"] * hauteur

        

        donnees_fondations.append(info)
        
    return donnees_fondations