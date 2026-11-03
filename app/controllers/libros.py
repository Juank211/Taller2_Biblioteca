from app.core.exceptions import RecursoNoEncontrado
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.autor import Autor
from app.models.categoria import Categoria
from app.models.libro import Libro
from app.schemas.libro import LibroCreate as LibroIn

def crear_libro(datos: LibroIn, db: Session):
    if db.get(Autor, datos.autor_id) is None:
        raise RecursoNoEncontrado("Autor no encontrado")

    categorias = db.scalars(select(Categoria).where(Categoria.id.in_(datos.categoria_ids))).all()
    if len(categorias) != len(datos.categoria_ids):
        raise RecursoNoEncontrado("Una o más categorías no fueron encontradas")

    datos_dict = datos.model_dump(exclude={"categoria_ids"})
    libro = Libro(**datos_dict)
    libro.categorias = list(categorias)
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro

def listar_libros(disponible: bool | None, db: Session):
    consulta = select(Libro).order_by(Libro.id)
    libros = list(db.scalars(consulta).all())
    if disponible is True:
        libros = [l for l in libros if l.disponibles > 0]
    elif disponible is False:
        libros = [l for l in libros if l.disponibles == 0]
    return libros

def actualizar_libro(libro_id: int, datos: LibroIn, db: Session):
    libro = db.get(Libro, libro_id)
    if libro is None:
        raise RecursoNoEncontrado("Libro no encontrado")

    if db.get(Autor, datos.autor_id) is None:
        raise RecursoNoEncontrado("Autor no encontrado")

    categorias = db.scalars(select(Categoria).where(Categoria.id.in_(datos.categoria_ids))).all()
    if len(categorias) != len(datos.categoria_ids):
        raise RecursoNoEncontrado("Una o más categorías no fueron encontradas")

    for campo, valor in datos.model_dump(exclude={"categoria_ids"}).items():
        setattr(libro, campo, valor)
    libro.categorias = list(categorias)

    db.commit()
    db.refresh(libro)
    return libro

def eliminar_libro(libro_id: int, db: Session):
    libro = db.get(Libro, libro_id)
    if libro is None:
        raise RecursoNoEncontrado("Libro no encontrado")

    db.delete(libro)
    db.commit()
