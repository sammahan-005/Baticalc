import ifcopenshell
import ifcopenshell.util.element

def parse_columns(model):
    """
    Extrait les données des poteaux (IfcColumn et IfcColumnStandardCase).
    """
    donnees_poteaux = []
    columns = model.by_type("IfcColumn")
    
    # Ajouter aussi les IfcColumnStandardCase (sous-classe de IfcColumn)
    columns.extend(model.by_type("IfcColumnStandardCase"))
    
    # Éliminer les doublons
    columns = list({col.id(): col for col in columns}.values())

    for column in columns:
        # Récupération des PropertySets
        psets = ifcopenshell.util.element.get_psets(column)
        qto = psets.get("BaseQuantities", {})
        
        # Récupération du type de poteau
        column_type = ifcopenshell.util.element.get_type(column)
        
        # Récupération du niveau
        niveau = ifcopenshell.util.element.get_container(column)
        
        # Calculs de base
        hauteur = qto.get("Height", 0) or _extraire_hauteur_depuis_geometrie(column)
        
        # Extraction des dimensions transversales
        largeur_x = qto.get("Width", 0)  # Dimension en X (souvent largeur)
        largeur_y = qto.get("Depth", 0)  # Dimension en Y (souvent profondeur)
        
        # Si Depth n'existe pas, essayer d'autres noms
        if largeur_y == 0:
            largeur_y = qto.get("Length", 0)
        
        # Surface transversale et volume
        surface_transversale = largeur_x * largeur_y if largeur_x > 0 and largeur_y > 0 else 0
        volume = surface_transversale * hauteur if hauteur > 0 else qto.get("NetVolume", 0)
        
        # Surface de coffrage (périmètre × hauteur)
        perimetre = 2 * (largeur_x + largeur_y) if largeur_x > 0 and largeur_y > 0 else 0
        surface_coffrage = perimetre * hauteur if hauteur > 0 else 0
        
        info = {
            
            "guid": column.GlobalId,
            "nom": column_type.Name if column_type and column_type.Name else "Poteau sans nom",
            "type_ifc": column.is_a(),  # IfcColumn ou IfcColumnStandardCase
            
            
            "categorie": _categoriser_poteau(column, column_type, qto, niveau, largeur_x, largeur_y),
            "materiau_principal": _extraire_materiau_poteau(column) or "Non spécifié",
            
            
            "volume_net": volume,  # m³ (béton)
            "surface_nette": qto.get("NetSideArea", 0),  # m² (surface apparente)
            
            
            "hauteur": hauteur,  # m
            "largeur_x": largeur_x,  # m (dimension selon X)
            "largeur_y": largeur_y,  # m (dimension selon Y)
            "section": f"{largeur_x:.0f}x{largeur_y:.0f}" if largeur_x > 0 and largeur_y > 0 else "Section non définie",
            
            
            "surface_coffrage": surface_coffrage,  # m²
            "perimetre": perimetre,  # m
            "surface_transversale": surface_transversale,  # m²
            
            
            "niveau": niveau.Name if niveau else "RDC",
            "nb_ouvertures": 0,  # Les poteaux n'ont pas d'ouvertures
            "est_structural": _est_poteau_structural(column, column_type),
            
            
            "hauteur_hors_norme": hauteur > 3.5,  # Seuil différent des murs
            "section_importante": (largeur_x > 0.5 or largeur_y > 0.5),
            "zone_souterraine": _est_en_sous_sol(niveau)
        }
        
        
        if column.is_a("IfcColumnStandardCase"):
            infos_couches = _extraire_couches_poteau(column, hauteur, perimetre, surface_coffrage, qto)
            info.update(infos_couches)
        else:
            # Pour IfcColumn simple
            info.update({
                "composition": None,
                "volumes_par_materiau": {},
                "presence_armature_speciale": False,
                "details_constructifs": {
                    "type_poteau": "Poteau simple sans détail de couches"
                }
            })
        
        donnees_poteaux.append(info)
    
    return donnees_poteaux


def _extraire_hauteur_depuis_geometrie(column):
    """
    Extrait la hauteur du poteau à partir de sa géométrie si non disponible dans les quantités.
    """
    try:
        if hasattr(column, 'Representation') and column.Representation:
            for rep in column.Representation.Representations:
                if hasattr(rep, 'Items'):
                    for item in rep.Items:
                        # Recherche d'une boîte englobante ou d'extrusions
                        if hasattr(item, 'SweptArea') and hasattr(item, 'Depth'):
                            return item.Depth
                        # Pour les représentations simples
                        if hasattr(item, 'Bounds'):
                            bounds = item.Bounds
                            if bounds and len(bounds) > 0:
                                z_max = max(b.Z for b in bounds)
                                z_min = min(b.Z for b in bounds)
                                return z_max - z_min
    except:
        pass
    return 0


def _extraire_materiau_poteau(column):
    """
    Extrait le matériau du poteau.
    """
    try:
        materiau = ifcopenshell.util.element.get_material(column)
        if materiau:
            # Si c'est un objet, essayer de prendre le nom
            if hasattr(materiau, 'Name'):
                return materiau.Name
            elif hasattr(materiau, 'Material'):
                return materiau.Material.Name
            elif isinstance(materiau, str):
                return materiau
    except:
        pass
    return None


def _categoriser_poteau(column, column_type, qto, niveau, largeur_x, largeur_y):
    """
    Retourne la catégorie de devis du poteau.
    """
    # 1. Par type IFC
    if column_type:
        type_ifc = getattr(column_type, "PredefinedType", None)
        if type_ifc == "COLUMN":
            # Colonne standard
            pass
        elif type_ifc == "PILASTER":
            return "POTEAU_PILASTRE"
    
    # 2. Par localisation
    if niveau and niveau.Name:
        nom_niveau = niveau.Name.lower()
        if any(terme in nom_niveau for terme in ["sous-sol", "ss", "soussol", "cave", "keller", "basement"]):
            return "POTEAU_SOUS_SOL"
    
    # 3. Par dimensions (classification selon section)
    if largeur_x > 0 and largeur_y > 0:
        section_max = max(largeur_x, largeur_y)
        section_min = min(largeur_x, largeur_y)
        
        # Poteaux de structure
        if section_max >= 0.5:
            return "POTEAU_BETON_ARME_GROSSE_SECTION"
        elif section_max >= 0.3:
            return "POTEAU_BETON_ARME_SECTION_MOYENNE"
        elif section_max >= 0.2:
            return "POTEAU_BETON_ARME_PETITE_SECTION"
        
        # Poteaux métalliques
        if section_min < 0.1 and section_max > 0.1:
            return "POTEAU_METALLIQUE_PROFILE"
    
    # 4. Par hauteur
    hauteur = qto.get("Height", 0)
    if hauteur > 4.0:
        return "POTEAU_GRANDE_HAUTEUR"
    
    # 5. Si c'est un IfcColumnStandardCase avec isolation
    if column.is_a("IfcColumnStandardCase"):
        try:
            # Vérifier la présence d'isolation
            if _poteau_a_isolation(column):
                return "POTEAU_ISOLE"
        except:
            pass
    
    # 6. Défaut
    return "POTEAU_BETON_STANDARD"


def _poteau_a_isolation(column):
    """
    Vérifie si le poteau a une isolation (pour les poteaux extérieurs).
    """
    try:
        representation = column.Representation
        if representation:
            for rep in representation.Representations:
                for item in rep.Items:
                    if hasattr(item, 'Layers'):
                        for layer in item.Layers:
                            if hasattr(layer, 'Material') and layer.Material:
                                nom = layer.Material.Name.lower()
                                if any(term in nom for term in ["isol", "laine", "polystyrène"]):
                                    return True
    except:
        pass
    return False


def _est_poteau_structural(column, column_type):
    """
    Détermine si le poteau est structural (porteur) ou non.
    """
    # Par le nom
    if column_type and column_type.Name:
        nom = column_type.Name.lower()
        if any(term in nom for term in ["porteur", "structural", "structure", "load"]):
            return True
    
    # Par les propriétés
    try:
        psets = ifcopenshell.util.element.get_psets(column)
        if "Pset_ColumnCommon" in psets:
            if psets["Pset_ColumnCommon"].get("LoadBearing", False):
                return True
    except:
        pass
    
    # Par défaut, un poteau est considéré comme structural
    return True


def _extraire_couches_poteau(column, hauteur, perimetre, surface_coffrage, qto):
    """
    Extrait les données des couches pour un IfcColumnStandardCase.
    """
    result = {
        "composition": None,
        "volumes_par_materiau": {},
        "presence_armature_speciale": False,
        "details_constructifs": {}
    }
    
    try:
        representation = column.Representation
        if not representation:
            return result
        
        # Récupération des couches
        couches = []
        for rep in representation.Representations:
            for item in rep.Items:
                if hasattr(item, 'Layers'):
                    couches.extend(item.Layers)
                    break
        
        if not couches:
            return result
        
        # Analyse détaillée des couches
        details_couches = []
        volumes_par_materiau = {}
        epaisseur_isolation = 0
        presence_armature = False
        
        for i, layer in enumerate(couches):
            nom_materiau = "Inconnu"
            if hasattr(layer, 'Material') and layer.Material:
                nom_materiau = layer.Material.Name or "Matériau sans nom"
            
            epaisseur = getattr(layer, 'LayerThickness', 0)
            
           
            # Calcul du volume (surface de coffrage × épaisseur)
            volume = surface_coffrage * epaisseur if surface_coffrage > 0 else 0
            
            # Stockage par matériau
            if nom_materiau not in volumes_par_materiau:
                volumes_par_materiau[nom_materiau] = 0
            volumes_par_materiau[nom_materiau] += volume
            
            # Détection d'isolation
            if type_couche == "isolation":
                epaisseur_isolation += epaisseur
            
            # Détection d'armature spéciale
            if any(term in nom_materiau.lower() for term in ["armature", "fer", "acier"]):
                presence_armature = True
            
            details_couches.append({
                "nom": nom_materiau,
                "epaisseur": epaisseur,
                "type": type_couche,
                "volume": volume
            })
        
        result.update({
            "composition": {
                "couches": details_couches,
                "nb_couches": len(details_couches),
                "epaisseur_totale": sum(c["epaisseur"] for c in details_couches)
            },
            "volumes_par_materiau": volumes_par_materiau,
            "presence_armature_speciale": presence_armature,
            "details_constructifs": {
                "epaisseur_isolation": epaisseur_isolation,
                "type_poteau": "Poteau avec couches" if details_couches else "Poteau standard"
            }
        })
        
    except Exception as e:
        result["details_constructifs"]["erreur"] = str(e)
    
    return result





def _est_en_sous_sol(niveau):
    """
    Détermine si l'élément est en zone souterraine.
    """
    if not niveau or not niveau.Name:
        return False
    nom_niveau = niveau.Name.lower()
    return any(terme in nom_niveau for terme in [
        "sous-sol", "ss", "soussol", "cave", "keller", "basement", "subsol"
    ])


def analyser_fichier_ifc_poteaux(chemin_fichier):
    """
    Fonction principale pour analyser les poteaux d'un fichier IFC.
    """
    try:
        model = ifcopenshell.open(chemin_fichier)
        return parse_columns(model)
    except Exception as e:
        print(f"Erreur d'ouverture : {e}")
        return []