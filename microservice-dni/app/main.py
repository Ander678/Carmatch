from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .models import DNIRequest, PersonaResponse, ErrorResponse
from .service import DNIService
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Microservicio de Consulta DNI",
    description="API para consultar información de personas por DNI (RENIEC)",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicio
dni_service = DNIService()

@app.get("/")
def root():
    return {
        "service": "Microservicio DNI",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Endpoint de health check"""
    return {"status": "healthy"}

@app.post(
    "/consultar-dni",
    response_model=PersonaResponse,
    responses={
        200: {"description": "Consulta exitosa"},
        400: {"model": ErrorResponse, "description": "DNI inválido"},
        404: {"model": ErrorResponse, "description": "DNI no encontrado"},
        500: {"model": ErrorResponse, "description": "Error del servidor"}
    }
)
def consultar_dni(request: DNIRequest):
    """
    Consulta información de una persona por DNI
    
    - **dni**: Número de DNI de 8 dígitos
    """
    try:
        resultado = dni_service.buscar_por_dni(request.dni)
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get(
    "/consultar-dni/{dni}",
    response_model=PersonaResponse,
    responses={
        200: {"description": "Consulta exitosa"},
        400: {"model": ErrorResponse, "description": "DNI inválido"},
        404: {"model": ErrorResponse, "description": "DNI no encontrado"},
        500: {"model": ErrorResponse, "description": "Error del servidor"}
    }
)
def consultar_dni_get(dni: str):
    """
    Consulta información de una persona por DNI (método GET)
    
    - **dni**: Número de DNI de 8 dígitos
    """
    if len(dni) != 8 or not dni.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El DNI debe tener 8 dígitos numéricos"
        )
    
    try:
        resultado = dni_service.buscar_por_dni(dni)
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVICE_PORT", 8001))
    host = os.getenv("SERVICE_HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)