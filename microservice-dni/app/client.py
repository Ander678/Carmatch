import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

load_dotenv()

class DNIClient:
    def __init__(self):
        self.api_token = os.getenv("API_TOKEN")
        self.base_url = "https://api.apis.net.pe/v1"
        
        if not self.api_token:
            raise ValueError("API_TOKEN no configurado en .env")
    
    def consultar_dni(self, dni: str) -> Dict[Any, Any]:
        """
        Consulta información de una persona por DNI usando apis.net.pe
        
        Args:
            dni: Número de DNI de 8 dígitos
            
        Returns:
            Diccionario con los datos de la persona
            
        Raises:
            requests.HTTPError: Si hay error en la consulta
        """
        url = f"{self.base_url}/dni?numero={dni}"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error al consultar DNI: {str(e)}")
    
    def consultar_ruc(self, ruc: str) -> Optional[Dict[Any, Any]]:
        """
        Consulta información de un RUC en SUNAT
        
        Args:
            ruc: Número de RUC (10 u 11 dígitos)
            
        Returns:
            Diccionario con los datos del RUC o None si no existe
        """
        url = f"{self.base_url}/ruc?numero={ruc}"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Verificar si el RUC existe y está activo
            if data.get("estado") in ["ACTIVO", "BAJA PROVISIONAL", "BAJA DEFINITIVA"]:
                return data
            return None
        except requests.exceptions.RequestException:
            # Si falla la consulta, asumimos que no existe
            return None