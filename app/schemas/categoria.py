from pydantic import BaseModel, ConfigDict, Field

class CategoriaIn(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    descripcion: str | None = Field(default=None, max_length=300)

class CategoriaOut(CategoriaIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
