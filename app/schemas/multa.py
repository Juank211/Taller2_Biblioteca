from pydantic import BaseModel, ConfigDict
from typing import Optional

class MultaBase(BaseModel):
    usuario_id: int
    prestamo_id: int
    monto: float
    pagado: Optional[bool] = False

class MultaCreate(MultaBase):
    pass

class MultaUpdate(BaseModel):
    monto: Optional[float] = None
    pagado: Optional[bool] = None

class MultaResponse(MultaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
