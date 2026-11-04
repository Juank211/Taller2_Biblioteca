from pydantic import BaseModel, ConfigDict
from typing import Optional

class LibroBase(BaseModel):
    titulo: str
    autor: str
    isbn: str
    copias_disponibles: int
    estado: str

class LibroCreate(LibroBase):
    pass

class LibroOut(LibroBase):
    id: int
    portada_url: Optional[str] = None
    portada_public_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class LibroResponse(LibroOut):
    pass

class LibroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    isbn: Optional[str] = None
    copias_disponibles: Optional[int] = None
    estado: Optional[str] = None
    portada_url: Optional[str] = None
    portada_public_id: Optional[str] = None
