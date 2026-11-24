from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class PrestamoBase(BaseModel):
    libro_id: int
    usuario_id: Optional[int] = None
    estado: Optional[str] = "Activo"

class PrestamoCreate(BaseModel):
    libro_id: int
    usuario_id: Optional[int] = None
    estado: Optional[str] = "Activo"

class PrestamoUpdate(BaseModel):
    fecha_devuelto: Optional[datetime] = None
    estado: Optional[str] = None

class PrestamoOut(BaseModel):
    id: int
    usuario_id: int
    libro_id: int
    fecha_prestamo: datetime
    fecha_devuelto: Optional[datetime] = None
    estado: str

    model_config = ConfigDict(from_attributes=True)

class PrestamoDetalleOut(BaseModel):
    id: int
    libro_id: int
    libro_titulo: str
    libro_autor: Optional[str] = None
    libro_portada_url: Optional[str] = None
    usuario_id: int
    usuario_nombre: str
    usuario_email: str
    fecha_prestamo: datetime
    fecha_limite: datetime
    fecha_devuelto: Optional[datetime] = None
    estado: str
    dias_restantes: int
    vencido: bool
    dias_retraso: int
    multa_estimada: float

    model_config = ConfigDict(from_attributes=True)
