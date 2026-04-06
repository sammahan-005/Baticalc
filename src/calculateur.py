import sqlite3
import math
import sys
import os
from base_de_donnees import get_connection




def calculer_quantites_fondations(projet_id, ratio_acier=90):
    """
    Calcule les quantités pour les fondations.
    Utilise perimetre * hauteur pour le coffrage latéral selon l'extraction IFC.
    """
    conn= get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COALESCE(SUM(surface_base), 0.0), 
            COALESCE(SUM(volume), 0.0), 
            COALESCE(SUM(perimetre * hauteur), 0.0) 
        FROM fondations
        WHERE projet_id = ?
    """, (projet_id,))
    
    surface_base, volume, coffrage = cursor.fetchone()

    return {
        "Béton de propreté (m2)": round(surface_base, 2),
        "Béton armé (m3)": round(volume, 2),
        "Coffrage (m2)": round(coffrage, 2),
        "Aciers (kg)": round(volume * ratio_acier, 2)
    }


def calculer_quantites_elevations( projet_id):
    """
    Calcule les quantités pour les élévations (Murs et Cloisons).
    """

    conn= get_connection()
    cursor = conn.cursor()
    # On délègue le calcul du chaînage directement à SQL pour plus d'efficacité
    cursor.execute("""
        SELECT 
            COALESCE(SUM(surface), 0.0),
            COALESCE(SUM(CASE WHEN hauteur > 0 THEN surface / hauteur ELSE 0 END), 0.0)
        FROM murs
        WHERE projet_id = ?
    """, (projet_id,))
    
    surface_totale, longueur_chainage = cursor.fetchone()

    return {
        "Maçonnerie (m2)": round(surface_totale, 2),
        "Enduit intérieur/ext (m2)": round(surface_totale * 2, 2),
        "Chainage horizontal (m)": round(longueur_chainage, 2),
        "Peinture (m2)": round(surface_totale * 2, 2)
    }

def calculer_quantites_structure( projet_id, ratio_acier=135):
    """
    Calcule les quantités pour la structure (Poteaux / Colonnes).
    """

    conn= get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COALESCE(volume_net, 0.0), 
            COALESCE(surface_section, 0.0), 
            COALESCE(hauteur, 0.0)
        FROM poteaux
        WHERE projet_id = ?
    """, (projet_id,))
    
    volume_total = 0.0
    coffrage_total = 0.0

    for vol, surf, haut in cursor.fetchall():
        volume_total += vol
        # Estimation du périmètre pour coffrage (carré parfait assumé par défaut)
        perimetre_estime = 4 * math.sqrt(surf) if surf > 0 else 0
        coffrage_total += (perimetre_estime * haut)

    return {
        "Béton armé (m3)": round(volume_total, 2),
        "Coffrage (m2)": round(coffrage_total, 2),
        "Aciers (kg)": round(volume_total * ratio_acier, 2)
    }

def calculer_quantites_toiture( projet_id):
    """
    Calcule les quantités pour la toiture et les dalles.
    """

    conn= get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COALESCE(SUM(surface_reelle), 0.0), 
            COALESCE(SUM(surface_horizontale), 0.0) 
        FROM toitures
        WHERE projet_id = ?
    """, (projet_id,))
    
    surface_reelle, surface_horizontale = cursor.fetchone()

    return {
        "Étanchéité / Couverture (m2)": round(surface_reelle, 2),
        "Charpente Projection (m2)": round(surface_horizontale, 2),
        "Faux-plafond (m2)": round(surface_horizontale, 2)
    }

def generer_synthese_projet( projet_id):

    conn= get_connection()
    return {
        "Fondations": calculer_quantites_fondations(conn, projet_id),
        "Elevations": calculer_quantites_elevations(conn, projet_id),
        "Structure": calculer_quantites_structure(conn, projet_id),
        "Toiture": calculer_quantites_toiture(conn, projet_id)
    }

data = generer_synthese_projet(1)
print(data)    


def convertir_en_materiaux_et_estimer(synthese_quantites, prix_ref):
    """
    Convertit les quantités d'ouvrages en matériaux réels et calcule le coût.
    Basé sur des dosages standards (Béton dosé à 350kg/m3, etc.).
    """
    # Transformation de la liste de tuples prix_ref en dictionnaire pour accès rapide
    catalogue_prix = {item[0]: item[1] for item in prix_ref}
    
    # 1. Récupération des totaux globaux
    vol_beton_total = synthese_quantites["Fondations"]["Béton armé (m3)"] + synthese_quantites["Structure"]["Béton armé (m3)"]
    poids_acier_total = synthese_quantites["Fondations"]["Aciers (kg)"] + synthese_quantites["Structure"]["Aciers (kg)"]
    surface_murs = synthese_quantites["Elevations"]["Maçonnerie (m2)"]
    surface_toit_reelle = synthese_quantites["Toiture"]["Étanchéité / Couverture (m2)"]
    surface_toit_horiz = synthese_quantites["Toiture"]["Charpente Projection (m2)"]

    # 2. Règles de conversion (Dosages)
    besoins_materiaux = {
        "Sacs ciment 50kg": 0,
        "Sable (m3)": 0,
        "Gravier (m3)": 0,
        "Sable fin (m3)": 0,
        "Parpaings 20x20x40": 0,
        "Barres HA10 (12m)": 0,  # Utilisé comme moyenne représentative pour simplifier
        "Bac acier / couverture": surface_toit_reelle * 1.1, # +10% de recouvrement/chutes
        "Bois charpente (m3)": surface_toit_horiz * 0.05,    # Ratio estimatif m3 de bois par m2 de toiture
        "Clous / visserie (kg)": surface_toit_horiz * 0.15
    }

    # Béton armé (Dosage 350 kg/m3) -> 7 sacs de 50kg par m3
    besoins_materiaux["Sacs ciment 50kg"] += vol_beton_total * 7
    besoins_materiaux["Sable (m3)"] += vol_beton_total * 0.4
    besoins_materiaux["Gravier (m3)"] += vol_beton_total * 0.8

    # Maçonnerie (Parpaings + Mortier)
    besoins_materiaux["Parpaings 20x20x40"] += surface_murs * 12.5 # 12.5 parpaings/m2
    besoins_materiaux["Sacs ciment 50kg"] += surface_murs * 0.3    # Mortier de pose + enduit
    besoins_materiaux["Sable fin (m3)"] += surface_murs * 0.05

    # Aciers (Conversion kg -> barres. Ex: HA10 pèse environ 7.4 kg/barre de 12m)
    poids_moyen_barre_12m = 7.4 
    besoins_materiaux["Barres HA10 (12m)"] += (poids_acier_total / poids_moyen_barre_12m) * 1.05 # +5% de chutes

    # 3. Calcul du devis
    devis_detaille = {}
    cout_total = 0.0

    for materiau, quantite in besoins_materiaux.items():
        quantite_arrondie = math.ceil(quantite) if "Sacs" in materiau or "Parpaings" in materiau or "Barres" in materiau else round(quantite, 2)
        prix_unitaire = catalogue_prix.get(materiau, 0)
        total_ligne = quantite_arrondie * prix_unitaire
        
        devis_detaille[materiau] = {
            "Quantité": quantite_arrondie,
            "Prix Unitaire": prix_unitaire,
            "Total": total_ligne
        }
        cout_total += total_ligne

    return {
        "Devis Détaillé": devis_detaille,
        "Coût Total Matériaux": round(cout_total, 2)
    }    