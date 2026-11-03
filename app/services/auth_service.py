from datetime import datetime, timedelta
from fastapi import HTTPException
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models import Usuario, TokenNegro
from app.schemas import TokenData
from app.core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def obtener_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def crear_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire, "sub": data.get("email")})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def crear_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "sub": data.get("email")})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def revocar_token(db: Session, jti: str, expiracion: datetime) -> None:
    token_negro = TokenNegro(jti=jti, expiracion=expiracion)
    db.add(token_negro)
    db.commit()

def verificar_token_revocado(db: Session, jti: str) -> bool:
    return db.query(TokenNegro).filter(TokenNegro.jti == jti).first() is not None
