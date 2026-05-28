"""
FASE 1 – Punto de entrada de la aplicación
==========================================
Este es el archivo principal. Aquí:
  1. Se crea la instancia de FastAPI con metadatos para Swagger UI.
  2. Se incluyen los routers (grupos de rutas) de cada recurso.
  3. Se define una ruta raíz de bienvenida.

Para ejecutar:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from app.routes.user_routes import router as user_router

# ── Creación de la app ────────────────────────────────────────────────────────
# Los parámetros de FastAPI aparecen en Swagger UI (/docs)
app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la administración de usuarios del sistema device_systems. "
        "Permite listar, consultar y registrar usuarios con validaciones completas."
    ),
    version="1.0.0",
    contact={
        "name": "Equipo device_systems",
        "email": "soporte@devicesystems.com",
    },
)

# ── Registro de rutas ─────────────────────────────────────────────────────────
# Todas las rutas de user_router tendrán el prefijo /users
app.include_router(user_router)


# ── Ruta raíz ─────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    """Endpoint de bienvenida. Confirma que la API está funcionando."""
    return {
        "app": "device_systems",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online",
    }
