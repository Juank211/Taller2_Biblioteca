from pydantic import BaseModel, ConfigDict
from typing import Optional

class LibroBase(BaseModel):
    titulo: str
    autor: str
    isbn: str
    copias_disponibles: int
    estado: str
    portada_url: Optional[str] = None
    portada_public_id: Optional[str] = None

class LibroCreate(LibroBase):
    pass

class LibroOut(BaseModel):
    id: int
    titulo: str
    isbn: str
    portada_url: Optional[str] = None
    portada_public_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class LibroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    isbn: Optional[str] = None
    copias_disponibles: Optional[int] = None
    estado: Optional[str] = None
    portada_url: Optional[str] = None
    portada_public_id: Optional[str] = None

class LibroResponse(LibroBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
