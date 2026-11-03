from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Multa(Base):
    __tablename__ = "multas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    prestamo_id = Column(Integer, ForeignKey("prestamos.id"), nullable=False)
    monto = Column(Float, nullable=False)
    pagado = Column(Boolean, default=False)

    usuario = relationship("Usuario", back_populates="multas")
    prestamo = relationship("Prestamo", back_populates="multas")
