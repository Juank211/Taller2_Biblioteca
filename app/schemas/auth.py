from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    rol: Optional[str] = "usuario"
    email: Optional[str] = None
    nombre: Optional[str] = None

class TokenData(BaseModel):
    email: Optional[str] = None
    jti: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
