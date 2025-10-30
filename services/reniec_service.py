import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

def consultar_dni(dni):
    url = f"https://api.apis.net.pe/v1/dni?numero={dni}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
