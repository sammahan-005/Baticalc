import sqlite3
import math

def calculer_quantites_fondations(conn, projet_id, ratio_acier=90):
    """
    Calcule les quantités pour les fondations (Semelles isolées / Filantes).
    Ratio_acier par défaut : 90 kg/m3 (moyenne entre 80 et 100).
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            SUM(surface_base), 
            SUM(volume), 
            SUM(surface_coffrage_lateral) 
        FROM fondations
        WHERE projet_id = ?
    """, (projet_id,))
    
    result = cursor.fetchone()
    
    surface_base = result[0] or 0.0
    volume = result[1] or 0.0
    
    # Si surface_coffrage_lateral n'est pas pré-calculée en DB, on peut aussi 
    # utiliser SUM(perimetre * hauteur) directement dans la requête SQL.
    coffrage = result[2] or 0.0

    return {
        "Béton de propreté (m2)": round(surface_base, 2),
        "Béton armé (m3)": round(volume, 2),
        "Coffrage (m2)": round(coffrage, 2),
        "Aciers (kg)": round(volume * ratio_acier, 2)
    }

def calculer_quantites_elevations(conn, projet_id):
    """
    Calcule les quantités pour les élévations (Murs et Cloisons).
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT surface, hauteur
        FROM murs
        WHERE projet_id = ?
    """, (projet_id,))
    
    rows = cursor.fetchall()
    
    surface_totale = 0.0
    longueur_chainage = 0.0

    for surface, hauteur in rows:
        surf = surface or 0.0
        haut = hauteur or 0.0
        
        surface_totale += surf
        
        # Prévention de la division par zéro
        if haut > 0:
            longueur_chainage += (surf / haut)

    return {
        "Maçonnerie (m2)": round(surface_totale, 2),
        "Enduit intérieur/ext (m2)": round(surface_totale * 2, 2),
        "Chainage horizontal (m)": round(longueur_chainage, 2),
        "Peinture (m2)": round(surface_totale * 2, 2)
    }

def calculer_quantites_structure(conn, projet_id, ratio_acier=135):
    """
    Calcule les quantités pour la structure (Poteaux / Colonnes).
    Ratio_acier par défaut : 135 kg/m3 (moyenne entre 120 et 150).
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT volume_net, surface_section, hauteur
        FROM poteaux
        WHERE projet_id = ?
    """, (projet_id,))
    
    rows = cursor.fetchall()
    
    volume_total = 0.0
    coffrage_total = 0.0

    for vol_net, surf_section, hauteur in rows:
        vol = vol_net or 0.0
        surf = surf_section or 0.0
        haut = hauteur or 0.0
        
        volume_total += vol
        
        # Note technique : La table 'poteaux' n'a pas de champ 'perimetre'.
        # Pour le coffrage, on l'estime en supposant une section carrée : P = 4 * sqrt(Surface)
        perimetre_estime = 4 * math.sqrt(surf) if surf > 0 else 0
        coffrage_total += (perimetre_estime * haut)

    return {
        "Béton armé (m3)": round(volume_total, 2),
        "Coffrage (m2)": round(coffrage_total, 2),
        "Aciers (kg)": round(volume_total * ratio_acier, 2)
    }

def calculer_quantites_toiture(conn, projet_id):
    """
    Calcule les quantités pour la toiture et les dalles.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            SUM(surface_reelle), 
            SUM(surface_horizontale) 
        FROM toitures
        WHERE projet_id = ?
    """, (projet_id,))
    
    result = cursor.fetchone()
    
    surface_reelle = result[0] or 0.0
    surface_horizontale = result[1] or 0.0

    return {
        "Étanchéité / Couverture (m2)": round(surface_reelle, 2),
        "Charpente Projection (m2)": round(surface_horizontale, 2),
        "Faux-plafond (m2)": round(surface_horizontale, 2)
    }

def generer_synthese_projet(conn, projet_id):
    """
    Rassemble toutes les estimations dans un seul dictionnaire global.
    """
    return {
        "Fondations": calculer_quantites_fondations(conn, projet_id),
        "Elevations": calculer_quantites_elevations(conn, projet_id),
        "Structure": calculer_quantites_structure(conn, projet_id),
        "Toiture": calculer_quantites_toiture(conn, projet_id)
    }