from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Prestamo, Libro, Multa
from app.schemas import PrestamoCreate
from app.core.exceptions import ErrorAplicacion, RecursoNoEncontrado

class PrestamoService:
    @staticmethod
    def crear_prestamo(db: Session, prestamo: PrestamoCreate, usuario_id: int) -> Prestamo:
        libro = db.query(Libro).filter(Libro.id == prestamo.libro_id).first()
        if not libro:
            raise RecursoNoEncontrado("Libro no encontrado")

        if libro.copias_disponibles <= 0:
            raise ErrorAplicacion(
                status_code=400,
                detail="No hay copias disponibles de este libro"
            )

        libro.copias_disponibles -= 1
        db.add(libro)
        db.commit()

        prestamo_db = Prestamo(
            usuario_id=usuario_id,
            libro_id=prestamo.libro_id,
            estado=prestamo.estado
        )
        db.add(prestamo_db)
        db.commit()
        db.refresh(prestamo_db)
        return prestamo_db

    @staticmethod
    def devolver_prestamo(db: Session, prestamo_id: int, fecha_devuelto: datetime) -> Prestamo:
        prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
        if not prestamo:
            raise RecursoNoEncontrado("Préstamo no encontrado")

        libro = db.query(Libro).filter(Libro.id == prestamo.libro_id).first()
        if not libro:
            raise ErrorAplicacion(
                status_code=500,
                detail="Error al obtener libro"
            )

        libro.copias_disponibles += 1
        db.add(libro)
        db.commit()

        prestamo.fecha_devuelto = fecha_devuelto
        prestamo.estado = "Devolvido"
        db.commit()
        db.refresh(prestamo)

        # Verificar si hay multa por retraso
        if prestamo.fecha_devuelto and prestamo.fecha_prestamo:
            dias_retraso = (prestamo.fecha_devuelto - prestamo.fecha_prestamo).days
            if dias_retraso > 14:  # Ejemplo: multa si se superan 14 días
                monto_multa = dias_retraso - 14
                multa = Multa(
                    usuario_id=prestamo.usuario_id,
                    prestamo_id=prestamo.id,
                    monto=monto_multa,
                    pagado=False
                )
                db.add(multa)
                db.commit()

        return prestamo
