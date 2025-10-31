from .client import DNIClient
from .models import PersonaResponse
from typing import Dict, Any

class DNIService:
    def __init__(self):
        self.client = DNIClient()
    
    @staticmethod
    def calcular_digito_verificador_ruc10(dni: str) -> str:
        """
        Calcula el dígito verificador para RUC10 (persona natural)
        Algoritmo oficial de SUNAT
        """
        ruc_base = "10" + dni  # RUC10 = 10 + DNI
        
        # Factores de multiplicación
        factores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
        
        # Calcular suma ponderada
        suma = sum(int(ruc_base[i]) * factores[i] for i in range(10))
        
        # Calcular residuo
        residuo = suma % 11
        
        # Calcular dígito verificador
        digito = 11 - residuo
        
        if digito == 10:
            digito = 0
        elif digito == 11:
            digito = 1
        
        return str(digito)
    
    @staticmethod
    def generar_ruc10(dni: str) -> str:
        """Genera el RUC10 completo a partir del DNI"""
        digito = DNIService.calcular_digito_verificador_ruc10(dni)
        return f"10{dni}{digito}"
    
    def buscar_por_dni(self, dni: str) -> PersonaResponse:
        """
        Busca información de una persona por DNI
        
        Args:
            dni: Número de DNI
            
        Returns:
            PersonaResponse con los datos de la persona y su RUC10 si existe
        """
        # Consultar API de DNI
        data = self.client.consultar_dni(dni)
        
        # Generar RUC10 probable
        ruc10_generado = self.generar_ruc10(dni)
        
        # Verificar si el RUC10 existe en SUNAT
        ruc_data = self.client.consultar_ruc(ruc10_generado)
        tiene_ruc = ruc_data is not None
        
        # Transformar respuesta al modelo interno
        return PersonaResponse(
            dni=data.get("numeroDocumento", dni),
            nombres=data.get("nombres", ""),
            apellido_paterno=data.get("apellidoPaterno", ""),
            apellido_materno=data.get("apellidoMaterno", ""),
            ruc10=ruc10_generado if tiene_ruc else None,
            tiene_ruc=tiene_ruc
        )