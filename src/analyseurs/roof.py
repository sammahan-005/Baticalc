import ifcopenshell
import ifcopenshell.util.element

def parse_roofs(model):
    """
    Parcourt le modèle IFC pour extraire les données de devis de toutes les toitures
    (IfcRoof et IfcSlab typés ROOF).
    """
    donnees_toitures = []

    # 1. Sélection des éléments (Toitures natives et Dalles de type ROOF)
    roofs = model.by_type("IfcRoof")
    slabs = model.by_type("IfcSlab")
    
    # Filtrage des dalles qui servent de toiture
    roof_slabs = [s for s in slabs if ifcopenshell.util.element.get_type(s) and 
                  ifcopenshell.util.element.get_type(s).PredefinedType == "ROOF"]
    
    # Fusion des deux listes
    elements_a_traiter = roofs + roof_slabs

    # 2. Boucle d'extraction des données
    for element in elements_a_traiter:
        info = {
           
            "guid": element.GlobalId,
            "nom_instance": element.Name or "Toiture sans nom",
            "type_ifc": element.is_a(),
            "etage": "",
            "surface_horizontale": 0,
            "surface_reelle": 0,
            "pente_moyenne": 0,
            # "materiaux": []
        }

        # Localisation (Étage)
        container = ifcopenshell.util.element.get_container(element)
        if container:
            info["etage"] = container.Name

        # Extraction des quantités
        psets = ifcopenshell.util.element.get_psets(element)
        qto_names = ["Qto_RoofBaseQuantities", "Qto_SlabBaseQuantities", "Pset_Revit_Dimensions"]
        
        for name in qto_names:
            if name in psets:
                qto = psets[name]
                info["surface_horizontale"] = qto.get("GrossArea", qto.get("Area", 0))
                info["surface_reelle"] = qto.get("NetArea", info["surface_horizontale"])
                break

        # Extraction de la pente
        common_set = psets.get("Pset_RoofCommon", psets.get("Pset_SlabCommon", {}))
        info["pente_moyenne"] = common_set.get("Slope", 0)

        # Matériaux
        # material_assoc = ifcopenshell.util.element.get_material(element)
        # if material_assoc:
        #     if hasattr(material_assoc, "Materials"):
        #         info["materiaux"] = [m.Name for m in material_assoc.Materials]
        #     elif hasattr(material_assoc, "Name"):
        #         info["materiaux"] = [material_assoc.Name]

        donnees_toitures.append(info)

    return donnees_toitures




# chemin_fichier="/home/mahan-samuel/Téléchargements/Test8.ifc"
# model = ifcopenshell.open(chemin_fichier)
# data=parse_roofs(model)
# print(data[3]) 