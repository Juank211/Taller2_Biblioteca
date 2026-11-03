from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.database import Base

# Tabla de asociación para la relación muchos a muchos entre Libro y Categoria
libro_categoria = Table(
    "libro_categoria",
    Base.metadata,
    Column("libro_id", Integer, ForeignKey("libros.id"), primary_key=True),
    Column("categoria_id", Integer, ForeignKey("categorias.id"), primary_key=True)
)
