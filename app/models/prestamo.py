from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    libro_id = Column(Integer, ForeignKey("libros.id"), nullable=False)
    fecha_prestamo = Column(DateTime, server_default=func.now())
    fecha_devuelto = Column(DateTime, nullable=True)
    estado = Column(String, nullable=False)

    usuario = relationship("Usuario", back_populates="prestamos")
    libro = relationship("Libro", back_populates="prestamos")
    multas = relationship("Multa", back_populates="prestamo", cascade="all, delete-orphan")
