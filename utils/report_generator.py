from services.reniec_service import consultar_dni
from services.sunat_service import consultar_ruc

def generar_reporte(dni, ruc=None):
    try:
        print("Consultando datos del vendedor (RENIEC)...")
        datos_vendedor = consultar_dni(dni)
        nombre = f"{datos_vendedor.get('nombres', '')} {datos_vendedor.get('apellidoPaterno', '')} {datos_vendedor.get('apellidoMaterno', '')}".strip()
        print(f"✅ Vendedor encontrado: {nombre}")

        datos_empresa = None
        if ruc:
            print("\nConsultando datos de la empresa (SUNAT)...")
            datos_empresa = consultar_ruc(ruc)
            razon_social = datos_empresa.get("razonSocial") or datos_empresa.get("nombre") or "No disponible"
            print(f"✅ Empresa: {razon_social}")
        else:
            print("\n⚠️ No se ingresó RUC, se omite la consulta a SUNAT.")
            razon_social = None

        reporte = {
            "datosVendedor": {
                "nombre": nombre,
                "numeroDocumento": datos_vendedor.get("numeroDocumento", ""),
                "estado": datos_vendedor.get("estado", ""),
                "direccion": datos_vendedor.get("direccion", ""),
                "provincia": datos_vendedor.get("provincia", ""),
                "departamento": datos_vendedor.get("departamento", "")
            },
            "datosEmpresa": None if not datos_empresa else {
                "nombre": razon_social,
                "numeroDocumento": datos_empresa.get("numeroDocumento", ""),
                "estado": datos_empresa.get("estado", ""),
                "condicion": datos_empresa.get("condicion", ""),
                "direccion": datos_empresa.get("direccion", ""),
                "distrito": datos_empresa.get("distrito", ""),
                "provincia": datos_empresa.get("provincia", ""),
                "departamento": datos_empresa.get("departamento", "")
            }
        }

        print("\n📄 REPORTE CONSOLIDADO GENERADO ✅")
        return reporte

    except Exception as e:
        print("❌ Error general:", str(e))
        return None
