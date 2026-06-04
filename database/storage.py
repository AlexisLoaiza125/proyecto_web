import os
import requests
from fastapi import HTTPException

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET = "fitness-media"

def subir_imagen(archivo_bytes: bytes, nombre_archivo: str, carpeta: str) -> str:
    """Sube directamente via REST API de Supabase Storage sin usar el cliente Python."""
    ruta = f"{carpeta}/{nombre_archivo}"
    url_upload = f"{SUPABASE_URL}/storage/v1/object/{BUCKET}/{ruta}"
    
    headers = {
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "apikey": SUPABASE_KEY,
        "Content-Type": "image/jpeg",
        "x-upsert": "true"
    }
    
    res = requests.post(url_upload, headers=headers, data=archivo_bytes)
    print(f"Status: {res.status_code} — {res.text}")
    
    if res.status_code not in (200, 201):
        raise HTTPException(500, f"Error subiendo imagen: {res.text}")
    
    url_publica = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{ruta}"
    print(f"✅ URL: {url_publica}")
    return url_publica