import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

def consultar_ruc(ruc):
    url = f"https://api.apis.net.pe/v1/ruc?numero={ruc}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
