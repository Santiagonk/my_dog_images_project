from fastapi import FastAPI
import subprocess


app = FastAPI()


@app.get("/start_download")
async def start_download():
    # Ejecuta el script de descarga de imágenes
    subprocess.Popen(["python", "app/app.py"])
    return {"message": "Descarga iniciada"}


@app.get("/status")
async def status():
    # Devuelve el estado del proceso de descarga
    return {"status": "En ejecución"}
