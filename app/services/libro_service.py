from sqlalchemy.orm import Session
from app.models import Libro
from app.schemas import LibroCreate, LibroUpdate
from app.core.exceptions import ErrorAplicacion, RecursoNoEncontrado

class LibroService:
    @staticmethod
    def crear_libro(db: Session, libro: LibroCreate) -> Libro:
        db_libro = db.query(Libro).filter(Libro.isbn == libro.isbn).first()
        if db_libro:
            raise ErrorAplicacion(
                status_code=400,
                detail="El ISBN ya está registrado"
            )

        db_libro = Libro(
            titulo=libro.titulo,
            autor=libro.autor,
            isbn=libro.isbn,
            copias_disponibles=libro.copias_disponibles,
            estado=libro.estado
        )
        db.add(db_libro)
        db.commit()
        db.refresh(db_libro)
        return db_libro

    @staticmethod
    def obtener_libro(db: Session, libro_id: int) -> Libro:
        libro = db.query(Libro).filter(Libro.id == libro_id).first()
        if not libro:
            raise RecursoNoEncontrado("Libro no encontrado")
        return libro

    @staticmethod
    def actualizar_libro(db: Session, libro_id: int, libro: LibroUpdate) -> Libro:
        db_libro = db.query(Libro).filter(Libro.id == libro_id).first()
        if not db_libro:
            raise RecursoNoEncontrado("Libro no encontrado")

        if libro.titulo:
            db_libro.titulo = libro.titulo
        if libro.autor:
            db_libro.autor = libro.autor
        if libro.isbn:
            if db.query(Libro).filter(Libro.isbn == libro.isbn, Libro.id != libro_id).first():
                raise ErrorAplicacion(
                    status_code=400,
                    detail="El ISBN ya está registrado"
                )
            db_libro.isbn = libro.isbn
        if libro.copias_disponibles is not None:
            db_libro.copias_disponibles = libro.copias_disponibles
        if libro.estado:
            db_libro.estado = libro.estado

        db.commit()
        db.refresh(db_libro)
        return db_libro

    @staticmethod
    def eliminar_libro(db: Session, libro_id: int) -> None:
        libro = db.query(Libro).filter(Libro.id == libro_id).first()
        if not libro:
            raise RecursoNoEncontrado("Libro no encontrado")
        db.delete(libro)
        db.commit()
