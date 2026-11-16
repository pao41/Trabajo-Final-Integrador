from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.alumnos.ficha_router import router as ficha_router
from app.modules.alumnos.router import router as alumnos_router
from app.modules.configuracion.router import router as configuracion_router
from app.modules.planes.inscripcion_router import router as inscripciones_router
from app.modules.planes.router import router as planes_router
from app.modules.salud.router import router as salud_router
from app.modules.usuarios.router import auth_router
from app.modules.usuarios.router import router as usuarios_router

app = FastAPI(
    title="Sistema de Gestión para Gimnasios",
    description="API del TFI (Grupo 105). Documentación interactiva en /docs.",
    version="0.1.0",
)

# El navegador solo puede llamar a la API desde el origen del frontend, enviando cookies
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(salud_router)
app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(alumnos_router)
app.include_router(ficha_router)
app.include_router(configuracion_router)
app.include_router(planes_router)
app.include_router(inscripciones_router)



