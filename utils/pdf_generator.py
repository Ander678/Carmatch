from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from datetime import datetime

def construir_tabla(datos):
    """Genera una lista de filas [Etiqueta, Valor] solo con los campos que tienen contenido."""
    etiquetas = {
        "nombre": "Nombre completo",
        "numeroDocumento": "DNI / RUC",
        "estado": "Estado",
        "condicion": "Condición",
        "direccion": "Dirección",
        "distrito": "Distrito",
        "provincia": "Provincia",
        "departamento": "Departamento"
    }

    tabla = []
    for campo, etiqueta in etiquetas.items():
        valor = datos.get(campo, "")
        if valor:  # Solo agrega si hay contenido
            tabla.append([etiqueta, valor])
    return tabla

def generar_reporte_pdf(reporte):
    """Genera un reporte PDF con los datos del vendedor y la empresa."""
    datos_vendedor = reporte.get("datosVendedor", {})
    # Handle case where datosEmpresa is None or missing
    datos_empresa = reporte.get("datosEmpresa", {}) if reporte.get("datosEmpresa") is not None else {}

    # Nombre del archivo PDF (con fecha y hora)
    nombre_archivo = f"Reporte_CarMatch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    # --- Título principal ---
    titulo = Paragraph("📋 Reporte CarMatch - Consulta de Vehículo Usado", styles["Title"])
    elements.append(titulo)
    elements.append(Spacer(1, 12))

    # --- Sección de Vendedor ---
    subtitulo_v = Paragraph("👤 Datos del Vendedor", styles["Heading2"])
    elements.append(subtitulo_v)
    elements.append(Spacer(1, 6))

    tabla_vendedor = construir_tabla(datos_vendedor)
    if tabla_vendedor:
        t_v = Table(tabla_vendedor, colWidths=[150, 350])
        t_v.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica")
        ]))
        elements.append(t_v)
    else:
        elements.append(Paragraph("Sin datos disponibles.", styles["Normal"]))

    elements.append(Spacer(1, 18))

    # --- Sección de Empresa ---
    subtitulo_e = Paragraph("🏢 Datos de la Empresa", styles["Heading2"])
    elements.append(subtitulo_e)
    elements.append(Spacer(1, 6))

    tabla_empresa = construir_tabla(datos_empresa)
    if tabla_empresa:
        t_e = Table(tabla_empresa, colWidths=[150, 350])
        t_e.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica")
        ]))
        elements.append(t_e)
    else:
        elements.append(Paragraph("Sin datos disponibles.", styles["Normal"]))

    elements.append(Spacer(1, 24))

    # --- Pie de página ---
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    footer = Paragraph(f"Generado automáticamente por CarMatch el {fecha}.", ParagraphStyle(
        name="Footer", fontSize=9, textColor=colors.grey, alignment=1
    ))
    elements.append(footer)

    # --- Generar PDF ---
    doc.build(elements)
    print(f"✅ Reporte PDF generado correctamente: {nombre_archivo}")

    return nombre_archivo