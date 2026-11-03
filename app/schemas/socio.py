from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr

class SocioIn(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    email: EmailStr
    telefono: str | None = Field(default=None, max_length=15)
    activo: bool = True

class SocioOut(SocioIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    fecha_alta: datetime
