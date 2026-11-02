import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.routes import usuarios, consultas

app = FastAPI(title="Registro de consultas de alumnos - IFTS 21")

# En Railway o Render: FRONTEND_ORIGIN=https://ifts21-form-consulta-prueba.netlify.app/
origenes = [x.strip() for x in os.getenv("FRONTEND_ORIGIN", "").split(",") if x.strip()]
if origenes:
    app.add_middleware(CORSMiddleware, allow_origins=origenes, allow_methods=["GET", "POST", "PATCH"], allow_headers=["Content-Type"])

app.include_router(usuarios.router)
app.include_router(consultas.router)

# En local, FastAPI sirve también el frontend; en producción Netlify lo sirve.
app.mount("/", StaticFiles(directory=Path(__file__).parent / "public", html=True), name="public")
