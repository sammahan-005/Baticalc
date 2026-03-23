import analyseurIfc
import walls
import foundations
import column
import roof

IFC_PATH = "/home/mahan-samuel/Bureau/Projets/BatiCalc/exemples_ifc/Test2.ifc"

def parseur(chemin_fichier):
    model = analyseurIfc.analyseur_fichier_ifc(chemin_fichier)#ouvrir le fichier 
    if model:
        
        donnees_murs = walls.parse_walls(model)
        #donnees_foundations = foundations.parse_foundations(model)
        #donnees_columns = column.parse_columns(model)
        #donnees-toit = roof.parse_roofs
        
        #return donnees_foundations
        #return donnees_murs
        return donnees_murs
    else:
        return 0

data=parseur(IFC_PATH)
print(data[0])