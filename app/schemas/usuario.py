from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: str
    activo: Optional[bool] = True

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None
    password: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: int
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)
