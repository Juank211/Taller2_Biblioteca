from pydantic import BaseModel, ConfigDict, Field

class AutorIn(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    nacionalidad: str = Field(min_length=1, max_length=100)
    anio_nacimiento: int

class AutorOut(AutorIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
