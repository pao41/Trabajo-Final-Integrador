from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.salud.router import router as salud_router

app = FastAPI(
    title="Sistema de Gestión para Gimnasios",
    description="API del TFI (Grupo 105). Documentación interactiva en /docs.",
    version="0.1.0",
)

# El navegador solo puede llamar a la API desde el origen del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(salud_router)
