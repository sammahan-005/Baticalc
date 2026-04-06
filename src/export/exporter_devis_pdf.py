# src/export/devis_exporter.py
import os
import math
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT


BLEU_FONCE  = colors.HexColor("#2c3e50")
BLEU_MID    = colors.HexColor("#3498db")
BLEU_CLAIR  = colors.HexColor("#d6eaf8")
VERT_FONCE  = colors.HexColor("#1e8449")   # Accent devis : ligne total
VERT_CLAIR  = colors.HexColor("#d5f5e3")   # Fond total général
GRIS_CLAIR  = colors.HexColor("#f8f9fa")
GRIS_MID    = colors.HexColor("#bdc3c7")
BLANC       = colors.white
ORANGE_SOFT = colors.HexColor("#fef9e7")   # Fond ligne zéro-prix


# ── Point d'entrée principal ─────────────────────────────────────────────────
def exporter_devis_pdf(
    resultat_devis: dict,
    nom_projet: str,
    nom_utilisateur: str,
    chemin_ifc: str,
    output_dir: str = "reports"
) -> str:
    """
    Génère un PDF de devis matériaux à partir du dict retourné par
    convertir_en_materiaux_et_estimer().

    Paramètres
    ----------
    resultat_devis   : dict avec clés "Devis Détaillé" et "Coût Total Matériaux"
    nom_projet       : nom affiché dans l'en-tête
    nom_utilisateur  : préparé par …
    chemin_ifc       : chemin du fichier IFC source (affiché dans l'en-tête)
    output_dir       : dossier de sortie (créé si absent)

    Retourne
    --------
    str : chemin absolu du fichier PDF généré
    """
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in nom_projet)
    output_path = os.path.join(output_dir, f"BATICALC_DEVIS_{safe}_{timestamp}.pdf")

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        rightMargin=1.5*cm, leftMargin=1.5*cm,
        topMargin=1.5*cm,   bottomMargin=1.5*cm,
        title=f"Devis Matériaux — {nom_projet}",
        author="BATICALC"
    )

    s = _styles()
    story = []

    # En-tête
    story += _header(nom_projet, chemin_ifc, nom_utilisateur, s)
    story.append(Spacer(1, 0.5*cm))

    # Corps : tableau du devis
    devis_detail = resultat_devis.get("Devis Détaillé", {})
    cout_total   = resultat_devis.get("Coût Total Matériaux", 0.0)
    story += _section_devis(devis_detail, cout_total, s)

    # Pied de page légal
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=GRIS_MID))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "Document généré par BATICALC — Calculateur BIM pour Gros Œuvre. "
        "Les quantités sont issues du modèle IFC et peuvent nécessiter vérification. "
        "Les prix sont indicatifs et basés sur le catalogue de référence fourni.",
        s["footer"]
    ))

    doc.build(story, onFirstPage=_page, onLaterPages=_page)
    return output_path


# ── En-tête ──────────────────────────────────────────────────────────────────
def _header(nom_projet, chemin_ifc, nom_utilisateur, s):
    now     = datetime.now().strftime("%d/%m/%Y à %H:%M")
    fichier = os.path.basename(chemin_ifc) if chemin_ifc else "—"
    W = A4[0] - 3*cm
    data = [
        [Paragraph("BATICALC", s["titre"])],
        [Paragraph("Devis Estimatif — Matériaux Gros Œuvre", s["sous"])],
        [Paragraph(f"Projet : {nom_projet}   |   Fichier IFC : {fichier}", s["meta"])],
        [Paragraph(f"Préparé par : {nom_utilisateur}   |   Date : {now}", s["meta"])],
    ]
    t = Table(data, colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), BLEU_FONCE),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
    ]))
    return [t]


# ── Section devis ────────────────────────────────────────────────────────────
def _section_devis(devis_detail: dict, cout_total: float, s) -> list:
    """Construit la bannière de titre + le tableau de devis + la ligne TOTAL."""
    if not devis_detail:
        return [Paragraph("Aucune ligne de devis à afficher.", s["small"])]

    W = A4[0] - 3*cm

    # ── Bannière bleue de section ────────────────────────────────────────────
    cat = Table(
        [[Paragraph("  DEVIS ESTIMATIF MATÉRIAUX", s["cell_b"])]],
        colWidths=[W]
    )
    cat.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), BLEU_MID),
        ("TEXTCOLOR",     (0, 0), (-1, -1), BLANC),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
    ]))

    # ── Colonnes : Désignation | Qté | Prix Unit. (FCFA) | Total (FCFA) ──────
    col_w = [7*cm, 2.5*cm, 3.5*cm, 3.5*cm]
    headers = ["Désignation", "Quantité", "Prix Unit. (FCFA)", "Montant (FCFA)"]

    all_rows = [[Paragraph(h, s["cell_b"]) for h in headers]]
    zero_price_rows = []   # indices des lignes sans prix (pour couleur d'alerte)

    for i, (materiau, info) in enumerate(devis_detail.items()):
        qte        = info.get("Quantité", 0)
        pu         = info.get("Prix Unitaire", 0)
        total_line = info.get("Total", 0)

        row = [
            Paragraph(materiau,               s["cell"]),
            Paragraph(_fmt_qte(qte),          s["cell_r"]),
            Paragraph(_fmt_prix(pu),          s["cell_r"]),
            Paragraph(_fmt_prix(total_line),  s["cell_r"]),
        ]
        all_rows.append(row)
        if pu == 0:
            zero_price_rows.append(i + 1)   # +1 à cause de la ligne d'en-tête

    # Ligne TOTAL
    all_rows.append([
        Paragraph("TOTAL GÉNÉRAL MATÉRIAUX", s["cell_total_label"]),
        Paragraph("",                         s["cell_r"]),
        Paragraph("",                         s["cell_r"]),
        Paragraph(_fmt_prix(cout_total),      s["cell_total_val"]),
    ])
    total_row_idx = len(all_rows) - 1

    dt = Table(all_rows, colWidths=col_w)

    # Style de base
    style_cmds = [
        ("BACKGROUND",    (0, 0),  (-1, 0),             BLEU_MID),
        ("TEXTCOLOR",     (0, 0),  (-1, 0),             BLANC),
        ("ROWBACKGROUNDS",(0, 1),  (-1, total_row_idx-1), [BLANC, GRIS_CLAIR]),
        ("GRID",          (0, 0),  (-1, -1),             0.4, GRIS_MID),
        ("TOPPADDING",    (0, 0),  (-1, -1),             4),
        ("BOTTOMPADDING", (0, 0),  (-1, -1),             4),
        ("LEFTPADDING",   (0, 0),  (-1, -1),             5),
        ("RIGHTPADDING",  (0, 0),  (-1, -1),             5),
        ("FONTNAME",      (0, 0),  (-1, 0),              "Helvetica-Bold"),
        # Ligne TOTAL
        ("BACKGROUND",    (0, total_row_idx), (-1, total_row_idx), VERT_CLAIR),
        ("LINEABOVE",     (0, total_row_idx), (-1, total_row_idx), 1.2, VERT_FONCE),
        ("SPAN",          (0, total_row_idx), (2, total_row_idx)),
    ]

    # Lignes sans prix → fond orange doux pour alerter
    for r in zero_price_rows:
        style_cmds.append(("BACKGROUND", (0, r), (-1, r), ORANGE_SOFT))

    dt.setStyle(TableStyle(style_cmds))

    elements = [cat, dt, Spacer(1, 0.5*cm)]

    # Note sur les lignes sans prix
    if zero_price_rows:
        elements.append(Paragraph(
            "⚠  Les lignes en jaune n'ont pas de prix unitaire dans le catalogue de référence "
            "et ne sont pas comptabilisées dans le total.",
            s["small"]
        ))
        elements.append(Spacer(1, 0.2*cm))

    return elements


# ── Helpers formatage ────────────────────────────────────────────────────────
def _fmt_prix(val) -> str:
    """Formate un montant en FCFA avec séparateur de milliers."""
    try:
        return f"{int(round(float(val))):,}".replace(",", " ")
    except (TypeError, ValueError):
        return "—"

def _fmt_qte(val) -> str:
    """Formate une quantité (entier ou flottant selon le cas)."""
    try:
        f = float(val)
        return str(int(f)) if f == int(f) else f"{f:.2f}"
    except (TypeError, ValueError):
        return "—"


# ── Styles ───────────────────────────────────────────────────────────────────
def _styles():
    return {
        "titre":  ParagraphStyle("titre",  fontSize=22, textColor=BLANC,
                                 fontName="Helvetica-Bold", alignment=TA_CENTER),
        "sous":   ParagraphStyle("sous",   fontSize=11, textColor=BLEU_CLAIR,
                                 fontName="Helvetica", alignment=TA_CENTER),
        "meta":   ParagraphStyle("meta",   fontSize=9,  textColor=BLEU_CLAIR,
                                 fontName="Helvetica", alignment=TA_CENTER),
        "cell":   ParagraphStyle("cell",   fontSize=8,  textColor=BLEU_FONCE,
                                 fontName="Helvetica"),
        "cell_r": ParagraphStyle("cell_r", fontSize=8,  textColor=BLEU_FONCE,
                                 fontName="Helvetica", alignment=TA_RIGHT),
        "cell_b": ParagraphStyle("cell_b", fontSize=8,  textColor=BLANC,
                                 fontName="Helvetica-Bold"),
        "cell_total_label": ParagraphStyle("ctl", fontSize=9, textColor=VERT_FONCE,
                                           fontName="Helvetica-Bold"),
        "cell_total_val":   ParagraphStyle("ctv", fontSize=9, textColor=VERT_FONCE,
                                           fontName="Helvetica-Bold", alignment=TA_RIGHT),
        "small":  ParagraphStyle("small",  fontSize=7.5, textColor=colors.grey,
                                 fontName="Helvetica-Oblique"),
        "footer": ParagraphStyle("footer", fontSize=7.5, textColor=colors.grey,
                                 fontName="Helvetica-Oblique", alignment=TA_CENTER),
    }


# ── Numérotation des pages ───────────────────────────────────────────────────
def _page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(A4[0] - 1.5*cm, 0.8*cm, f"Page {doc.page}")
    canvas.drawString(1.5*cm, 0.8*cm, "BATICALC — Devis Estimatif Matériaux")
    canvas.restoreState()


# ── Test rapide (facultatif) ─────────────────────────────────────────────────
if __name__ == "__main__":
    exemple_resultat = {
        "Devis Détaillé": {
            "Sacs ciment 50kg":      {"Quantité": 312,  "Prix Unitaire": 5000,   "Total": 1_560_000},
            "Sable (m3)":            {"Quantité": 17.84,"Prix Unitaire": 25000,  "Total": 446_000},
            "Gravier (m3)":          {"Quantité": 35.68,"Prix Unitaire": 30000,  "Total": 1_070_400},
            "Sable fin (m3)":        {"Quantité": 8.25, "Prix Unitaire": 25000,  "Total": 206_250},
            "Barres HA10 (12m)":     {"Quantité": 748,  "Prix Unitaire": 4200,   "Total": 3_141_600},
            "Parpaings 20x20x40":    {"Quantité": 2375, "Prix Unitaire": 350,    "Total": 831_250},
            "Bac acier / couverture":{"Quantité": 78.0, "Prix Unitaire": 8000,   "Total": 624_000},
            "Bois charpente (m3)":   {"Quantité": 3.0,  "Prix Unitaire": 180000, "Total": 540_000},
            "Clous / visserie (kg)": {"Quantité": 9.0,  "Prix Unitaire": 1500,   "Total": 13_500},
        },
        "Coût Total Matériaux": 8_433_000
    }

    path = exporter_devis_pdf(
        resultat_devis   = exemple_resultat,
        nom_projet       = "Villa Duplex RDC+1",
        nom_utilisateur  = "Ing. Jean-Paul Mvondo",
        chemin_ifc       = "/projets/villa_duplex.ifc",
        output_dir       = "reports"
    )
    print(f"PDF généré : {path}")