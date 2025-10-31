from pydantic import BaseModel, Field
from typing import Optional

class DNIRequest(BaseModel):
    dni: str = Field(..., min_length=8, max_length=8, description="DNI de 8 dígitos")

class PersonaResponse(BaseModel):
    dni: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    ruc10: Optional[str] = None  # RUC de persona natural (si existe)
    tiene_ruc: bool = False  # Indica si tiene RUC activo
    
    class Config:
        json_schema_extra = {
            "example": {
                "dni": "12345678",
                "nombres": "Juan",
                "apellido_paterno": "Pérez",
                "apellido_materno": "García",
                "ruc10": "10123456781",
                "tiene_ruc": True
            }
        }

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None