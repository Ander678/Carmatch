from services.reniec_service import consultar_dni
from services.sunat_service import consultar_ruc
from utils.report_generator import generar_reporte
from utils.pdf_generator import generar_reporte_pdf

if __name__ == "__main__":
    dni = input("Ingrese DNI del vendedor: ")
    ruc = input("Ingrese RUC de la empresa: ")

    reporte = generar_reporte(dni, ruc)

    if reporte:
        generar_reporte_pdf(reporte)
