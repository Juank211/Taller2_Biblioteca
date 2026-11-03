from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from .asociaciones import libro_categoria

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    copias_disponibles = Column(Integer, nullable=False)
    estado = Column(String, nullable=False)

    prestamos = relationship("Prestamo", back_populates="libro", cascade="all, delete-orphan")

    categorias: Mapped[list["Categoria"]] = relationship(
        secondary=libro_categoria,
        back_populates="libros",
        lazy="dynamic"
    )
