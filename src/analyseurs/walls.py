import ifcopenshell
import ifcopenshell.util.element

def parse_walls(model):
    donnees_murs = []
    walls = model.by_type("IfcWall")

    for wall in walls:
       
        info = {
            "guid": wall.GlobalId,
            "nom_instance": wall.Name,
            # "type_ifc": "NOTDEFINED",
            # "nom_technique": "Inconnu",
            
        }

        
        # if wall.IsTypedBy:
        #     rel = wall.IsTypedBy[0]
        #     wall_type = rel.RelatingType
            
            
        #     info["type_ifc"] = wall_type.PredefinedType if wall_type.PredefinedType else "NOTDEFINED"
        #     info["nom_technique"] = wall_type.Name if wall_type.Name else "Inconnu"

        
        psets = ifcopenshell.util.element.get_psets(wall)
        
       
        if "Qto_WallBaseQuantities" in psets:
            qto = psets["Qto_WallBaseQuantities"]
            info["surface"] = qto.get("NetSideArea", 0)
            info["volume"] = qto.get("NetVolume", 0)
            info["hauteur"] = qto.get("Height", 0)

       
        donnees_murs.append(info)
        
    return donnees_murs

