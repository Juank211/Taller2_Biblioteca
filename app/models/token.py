from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class TokenNegro(Base):
    __tablename__ = "lista_negra_tokens"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, nullable=False)
    expiracion = Column(DateTime, nullable=False)
    fecha_revocacion = Column(DateTime, server_default=func.now())
