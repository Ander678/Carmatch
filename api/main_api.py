from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

from services.reniec_service import consultar_dni
from services.sunat_service import consultar_ruc
from utils.report_generator import generar_reporte
from utils.pdf_generator import generar_reporte_pdf

app = FastAPI(title="CarMatch API")

# 🔹 Configurar carpetas para frontend
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/consultar")
async def consultar(dni: str, ruc: Optional[str] = None):
    try:
        reporte = generar_reporte(dni, ruc)
        if not reporte:
            return {"error": "No se pudo generar el reporte"}
        return reporte
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}

@app.post("/api/pdf")
async def generar_pdf(reporte: str = Form(...)):
    try:
        data = json.loads(reporte)
        pdf_path = generar_reporte_pdf(data)
        return FileResponse(
            pdf_path,
            filename="Reporte_CarMatch.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        return {"error": f"No se pudo crear el PDF: {str(e)}"}