"""
FASE 2 – Modelos de usuario con Pydantic
========================================
Aquí definimos:
  - UserCreate  → lo que recibe el POST (datos de entrada)
  - UserOut     → lo que devuelve la API  (datos de salida, oculta campos privados)
  - UserInDB    → representación interna con ID asignado
"""

from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal


# ── Modelo de ENTRADA (POST /users) ──────────────────────────────────────────
class UserCreate(BaseModel):
    name: str
    email: EmailStr          # Pydantic valida el formato de email automáticamente
    role: Literal["admin", "support", "user"]   # Solo estos 3 valores son válidos
    is_active: bool = True   # Por defecto el usuario está activo

    # Validación personalizada: name debe tener mínimo 3 caracteres
    @field_validator("name")
    @classmethod
    def name_min_length(cls, v: str) -> str:
        if len(v.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        return v.strip()


# ── Modelo INTERNO (con ID, se guarda en la "base de datos" en memoria) ───────
class UserInDB(UserCreate):
    id: int


# ── Modelo de SALIDA (response_model) ────────────────────────────────────────
# Solo exponemos los campos que queremos mostrar al cliente.
# Si en el futuro añadimos un campo "password", este modelo lo ocultaría.
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = {"from_attributes": True}
