# src/export/pdf_exporter.py
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.enums import TA_CENTER
from src.configuration import REPORTS_DIR

BLEU_FONCE = colors.HexColor("#2c3e50")
BLEU_MID   = colors.HexColor("#3498db")
BLEU_CLAIR = colors.HexColor("#d6eaf8")
GRIS_CLAIR = colors.HexColor("#f8f9fa")
GRIS_MID   = colors.HexColor("#bdc3c7")
BLANC      = colors.white


def exporter_pdf(rapport: dict, nom_projet: str,
                 nom_utilisateur: str, chemin_ifc: str,
                 output_dir: str = None) -> str:
    if output_dir is None:
        output_dir = REPORTS_DIR
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in nom_projet)
    output_path = os.path.join(output_dir, f"BATICALC_{safe}_{timestamp}.pdf")

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        rightMargin=1.5*cm, leftMargin=1.5*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
        title=f"Metre - {nom_projet}", author="BATICALC"
    )
    s = _styles()
    story = []
    story += _header(nom_projet, chemin_ifc, nom_utilisateur, s)
    story.append(Spacer(1, 0.5*cm))
    story += _section_murs(rapport.get("murs", []), s)
    story += _section_fondations(rapport.get("fondations", []), s)
    story += _section_poteaux(rapport.get("poteaux", []), s)
    story += _section_toitures(rapport.get("toitures", []), s)

    erreurs = rapport.get("erreurs", [])
    if erreurs:
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph("AVERTISSEMENTS", s["section"]))
        for e in erreurs:
            story.append(Paragraph(f"• {e}", s["small"]))

    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=GRIS_MID))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "Document genere par BATICALC — Calculateur BIM pour Gros Oeuvre. "
        "Les quantites sont extraites du modele IFC et peuvent necessiter verification.",
        s["footer"]
    ))
    doc.build(story, onFirstPage=_page, onLaterPages=_page)
    return output_path


def _styles():
    return {
        "titre":    ParagraphStyle("titre",    fontSize=22, textColor=BLANC,
                                   fontName="Helvetica-Bold", alignment=TA_CENTER),
        "sous":     ParagraphStyle("sous",     fontSize=11, textColor=BLEU_CLAIR,
                                   fontName="Helvetica", alignment=TA_CENTER),
        "meta":     ParagraphStyle("meta",     fontSize=9,  textColor=BLEU_CLAIR,
                                   fontName="Helvetica", alignment=TA_CENTER),
        "section":  ParagraphStyle("section",  fontSize=11, textColor=BLEU_FONCE,
                                   fontName="Helvetica-Bold", spaceBefore=4, spaceAfter=4),
        "cell":     ParagraphStyle("cell",     fontSize=8,  textColor=BLEU_FONCE,
                                   fontName="Helvetica"),
        "cell_b":   ParagraphStyle("cell_b",   fontSize=8,  textColor=BLEU_FONCE,
                                   fontName="Helvetica-Bold"),
        "small":    ParagraphStyle("small",    fontSize=8,  textColor=colors.grey,
                                   fontName="Helvetica"),
        "footer":   ParagraphStyle("footer",   fontSize=7.5, textColor=colors.grey,
                                   fontName="Helvetica-Oblique", alignment=TA_CENTER),
    }


def _header(nom_projet, chemin_ifc, nom_utilisateur, s):
    now = datetime.now().strftime("%d/%m/%Y a %H:%M")
    fichier = os.path.basename(chemin_ifc) if chemin_ifc else "—"
    W = A4[0] - 3*cm
    data = [
        [Paragraph("BATICALC", s["titre"])],
        [Paragraph("Tableau de Metre — Gros Oeuvre", s["sous"])],
        [Paragraph(f"Projet : {nom_projet}   |   Fichier IFC : {fichier}", s["meta"])],
        [Paragraph(f"Prepare par : {nom_utilisateur}   |   Date : {now}", s["meta"])],
    ]
    t = Table(data, colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), BLEU_FONCE),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
        ("RIGHTPADDING", (0,0),(-1,-1), 12),
    ]))
    return [t]


def _table_section(titre, headers, rows, col_w, s):
    if not rows:
        return []
    W = A4[0] - 3*cm
    cat = Table([[Paragraph(f"  {titre.upper()}", s["cell_b"])]], colWidths=[W])
    cat.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), BLEU_MID),
        ("TEXTCOLOR",    (0,0),(-1,-1), BLANC),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
    ]))
    all_rows = [[Paragraph(h, s["cell_b"]) for h in headers]]
    for r in rows:
        all_rows.append([Paragraph(str(v), s["cell"]) for v in r])
    dt = Table(all_rows, colWidths=col_w)
    dt.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), GRIS_CLAIR),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[BLANC, GRIS_CLAIR]),
        ("GRID",          (0,0),(-1,-1), 0.4, GRIS_MID),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
        ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
    ]))
    return [cat, dt, Spacer(1, 0.5*cm)]


def _section_murs(murs, s):
    headers = ["Nom", "Type IFC", "Materiau", "Surface (m2)", "Volume (m3)", "Hauteur (m)"]
    col_w   = [4*cm, 3*cm, 3.5*cm, 2.5*cm, 2.5*cm, 2*cm]
    rows = [[m.get("nom_instance","—"), m.get("type_ifc","—"), m.get("materiau","—"),
             f"{m.get('surface',0):.3f}", f"{m.get('volume',0):.3f}",
             f"{m.get('hauteur',0):.2f}"] for m in murs]
    return _table_section("Murs / Voiles", headers, rows, col_w, s)


def _section_fondations(fondations, s):
    headers = ["Nom", "Type", "Volume (m3)", "Surface (m2)", "Hauteur (m)", "Coffrage (m2)"]
    col_w   = [4*cm, 3*cm, 2.5*cm, 2.5*cm, 2*cm, 3.5*cm]
    rows = [[f.get("nom_instance","—"), f.get("nom_technique","—"),
             f"{f.get('volume',0):.3f}", f"{f.get('surface_base',0):.3f}",
             f"{f.get('hauteur',0):.2f}", f"{f.get('surface_coffrage_lateral',0):.3f}"]
            for f in fondations]
    return _table_section("Fondations", headers, rows, col_w, s)


def _section_poteaux(poteaux, s):
    headers = ["Nom", "Section", "Niveau", "Hauteur (m)", "Volume (m3)", "Coffrage (m2)"]
    col_w   = [4*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 3.5*cm]
    rows = [[p.get("nom","—"), p.get("section","—"), p.get("niveau","—"),
             f"{p.get('hauteur',0):.2f}", f"{p.get('volume_net',0):.3f}",
             f"{p.get('surface_coffrage',0):.3f}"] for p in poteaux]
    return _table_section("Poteaux", headers, rows, col_w, s)


def _section_toitures(toitures, s):
    headers = ["Nom", "Type", "Surface rampante (m2)", "Surface projetee (m2)", "Pente (deg)"]
    col_w   = [4*cm, 3.5*cm, 4*cm, 4*cm, 2*cm]
    rows = [[t.get("nom_instance","—"), t.get("type_ifc","—"),
             f"{t.get('surface_rampante',0):.3f}", f"{t.get('surface_projetee',0):.3f}",
             f"{t.get('pente',0):.1f}"] for t in toitures]
    return _table_section("Toitures", headers, rows, col_w, s)


def _page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(A4[0]-1.5*cm, 0.8*cm, f"Page {doc.page}")
    canvas.drawString(1.5*cm, 0.8*cm, "BATICALC — Rapport de Metre")
    canvas.restoreState()