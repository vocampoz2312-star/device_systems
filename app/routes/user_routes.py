"""
FASE 3, 4 y 5 – Endpoints GET, POST y cabeceras HTTP
=====================================================
Este archivo define todas las rutas del recurso /users.

Endpoints implementados:
  GET  /users                → Lista todos los usuarios (con filtros opcionales)
  GET  /users/{user_id}      → Obtiene un usuario por ID (Path Parameter)
  POST /users                → Crea un nuevo usuario

Query Parameters disponibles en GET /users:
  ?role=admin|support|user   → Filtra por rol
  ?is_active=true|false      → Filtra por estado activo/inactivo
"""

from fastapi import APIRouter, HTTPException, Query, Response
from typing import Optional

from app.schemas.user_schema import UserCreate, UserInDB, UserOut

# APIRouter agrupa las rutas; se "incluye" en main.py con un prefijo
router = APIRouter(prefix="/users", tags=["Usuarios"])


# ── "Base de datos" en memoria ────────────────────────────────────────────────
# Para este reto usamos una lista simple. En producción sería PostgreSQL, etc.
fake_db: list[UserInDB] = [
    UserInDB(id=1, name="Ana García",    email="ana@devicesystems.com",    role="admin",   is_active=True),
    UserInDB(id=2, name="Luis Herrera",  email="luis@devicesystems.com",   role="support", is_active=True),
    UserInDB(id=3, name="María López",   email="maria@devicesystems.com",  role="user",    is_active=False),
    UserInDB(id=4, name="Carlos Rueda",  email="carlos@devicesystems.com", role="user",    is_active=True),
]

# Contador para auto-incrementar el ID
_next_id = 5


def _add_custom_headers(response: Response) -> None:
    """FASE 5: Añade cabeceras personalizadas a todas las respuestas."""
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "1.0"


# ── GET /users ────────────────────────────────────────────────────────────────
@router.get("/", response_model=list[UserOut])
def list_users(
    response: Response,
    role: Optional[str]  = Query(None, description="Filtrar por rol: admin, support, user"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo (true/false)"),
):
    """
    Retorna la lista de usuarios.
    Se pueden combinar los filtros: /users?role=admin&is_active=true
    """
    _add_custom_headers(response)

    result = fake_db  # Empezamos con todos

    # Aplicamos filtros solo si el cliente los envió
    if role is not None:
        if role not in ("admin", "support", "user"):
            raise HTTPException(status_code=400, detail="Rol inválido. Usa: admin, support, user")
        result = [u for u in result if u.role == role]

    if is_active is not None:
        result = [u for u in result if u.is_active == is_active]

    return result


# ── GET /users/{user_id} ──────────────────────────────────────────────────────
@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, response: Response):
    """
    Retorna un usuario específico por su ID.
    Si no existe, devuelve 404.
    """
    _add_custom_headers(response)

    # Buscamos en la lista (en BD real sería un SELECT WHERE id = ?)
    user = next((u for u in fake_db if u.id == user_id), None)

    if user is None:
        raise HTTPException(status_code=404, detail=f"Usuario con id={user_id} no encontrado")

    return user


# ── POST /users ───────────────────────────────────────────────────────────────
@router.post("/", response_model=UserOut, status_code=201)
def create_user(user_data: UserCreate, response: Response):
    """
    Crea un nuevo usuario.
    - Valida los datos con Pydantic automáticamente.
    - Verifica que el email no esté duplicado.
    - Retorna el usuario creado con su ID asignado.
    """
    global _next_id
    _add_custom_headers(response)

    # Verificar email duplicado
    email_exists = any(u.email == user_data.email for u in fake_db)
    if email_exists:
        raise HTTPException(
            status_code=409,
            detail=f"El email '{user_data.email}' ya está registrado"
        )

    # Crear el usuario con ID asignado
    new_user = UserInDB(id=_next_id, **user_data.model_dump())
    _next_id += 1
    fake_db.append(new_user)

    return new_user
