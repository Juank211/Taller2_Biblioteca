from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Autor(Base):
    __tablename__ = "autores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    nacionalidad: Mapped[str] = mapped_column(String(100), nullable=False)
    anio_nacimiento: Mapped[int] = mapped_column(nullable=False)

    libros: Mapped[list["Libro"]] = relationship(back_populates="autor")
