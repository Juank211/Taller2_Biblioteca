from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class PrestamoBase(BaseModel):
    usuario_id: int
    libro_id: int
    estado: str

class PrestamoCreate(PrestamoBase):
    pass

class PrestamoUpdate(BaseModel):
    fecha_devuelto: Optional[datetime] = None
    estado: Optional[str] = None

class PrestamoResponse(PrestamoBase):
    id: int
    fecha_prestamo: datetime
    fecha_devuelto: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
