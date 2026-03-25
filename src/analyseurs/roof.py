import ifcopenshell
import ifcopenshell.util.element

def parse_roofs(model):
    donnees_toitures = []
    # On récupère les objets Toiture et les Dalles typées 'ROOF'
    roofs = model.by_type("IfcRoof")
    slabs = model.by_type("IfcSlab")
    
    # Filtrage des dalles qui servent de toiture (ex: toits plats ou pans isolés)
    roof_slabs = [s for s in slabs if ifcopenshell.util.element.get_type(s) and 
                  ifcopenshell.util.element.get_type(s).PredefinedType == "ROOF"]
    
    elements = roofs + roof_slabs

    for element in elements:
        
        info = {
            "guid": element.GlobalId,
            "nom_instance": element.Name or "Toiture sans nom",
            "type_ifc": "NOTDEFINED",
            "nom_technique": "Inconnu",
            "pente": 0,
            "materiau": "Non spécifié"
        }

        
        element_type = ifcopenshell.util.element.get_type(element)
        if element_type:
            info["type_ifc"] = getattr(element_type, "PredefinedType", "NOTDEFINED")
            info["nom_technique"] = element_type.Name or "Type inconnu"

        
        psets = ifcopenshell.util.element.get_psets(element)
        # On fusionne les sources possibles pour les toits et les dalles
        qto = {**psets.get("BaseQuantities", {}), 
               **psets.get("Qto_RoofBaseQuantities", {}), 
               **psets.get("Qto_SlabBaseQuantities", {})}
        
        
        info["surface_rampante"] = qto.get("GrossSurfaceArea", qto.get("NetArea", 0))
        # Surface au sol (projetée) pour la charpente/plafond
        info["surface_projetee"] = qto.get("ProjectedArea", 0)
        
       
        common = psets.get("Pset_RoofCommon") or psets.get("Pset_SlabCommon") or {}
        info["pente"] = common.get("Slope", 0)

       
        if info["type_ifc"] == "NOTDEFINED":
            nom_clean = info["nom_technique"].lower()
            if any(w in nom_clean for w in ["tuile", "tile"]):
                info["type_ifc"] = "COUVERTURE_TUILE"
            elif any(w in nom_clean for w in ["acier", "bac", "tole", "tôle"]):
                info["type_ifc"] = "COUVERTURE_METALLIQUE"
            elif "terrasse" in nom_clean:
                info["type_ifc"] = "TOIT_TERRASSE"

        donnees_toitures.append(info)
        
    return donnees_toitures