"""
Genera una plantilla en PDF para volcar la lista de empresas/leads que
necesitan servicios de produccion audiovisual (incluye columna para marcar
si es PYME). Pensada para llenarse con los resultados reales que produce
buscar_clientes_productora.py (leads_productora.csv / .json).

Uso:
    pip install reportlab
    python generar_plantilla_leads_pdf.py
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUTPUT_FILE = "leads_productora_plantilla.pdf"

styles = getSampleStyleSheet()
title_style = styles["Title"]
normal_style = styles["Normal"]

headers = ["Empresa", "PYME (Si/No)", "Necesidad audiovisual", "Contacto", "Fuente / URL"]
filler_rows = 25

data = [headers] + [["" for _ in headers] for _ in range(filler_rows)]

table = Table(
    data,
    colWidths=[5 * cm, 2.3 * cm, 5.5 * cm, 5 * cm, 6 * cm],
    repeatRows=1,
)

table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)

doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=landscape(letter),
    leftMargin=1.5 * cm,
    rightMargin=1.5 * cm,
)

elements = [
    Paragraph("Lista de prospectos: empresas que necesitan produccion audiovisual", title_style),
    Spacer(1, 0.3 * cm),
    Paragraph(
        "Plantilla para volcar los resultados de buscar_clientes_productora.py "
        "(empresas y PYMES en Mexico que requieren contenido corporativo / "
        "publicitario en video, foto o eventos).",
        normal_style,
    ),
    Spacer(1, 0.6 * cm),
    table,
]

doc.build(elements)
print(f"PDF generado: {OUTPUT_FILE}")
