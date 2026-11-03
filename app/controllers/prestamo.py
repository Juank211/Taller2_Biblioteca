from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.prestamo import Prestamo
from app.models.socio import Socio
from app.models.libro import Libro
from app.schemas.prestamo import PrestamoCreate
from app.core.exceptions import NoEncontrado, ReglaNegocio, Conflicto

def crear_prestamo(db: Session, datos: PrestamoCreate):
    # R1: Socio existe
    socio = db.get(Socio, datos.socio_id)
    if not socio:
        raise NoEncontrado("Socio no encontrado")
        
    # R2: Libro existe
    libro = db.get(Libro, datos.libro_id)
    if not libro:
        raise NoEncontrado("Libro no encontrado")

    # R3: Socio está activo
    if not socio.activo:
        raise ReglaNegocio("El socio no está activo")

    # R4: No tiene préstamos vencidos
    vencidos = db.scalar(
        select(func.count(Prestamo.id))
        .where(Prestamo.socio_id == datos.socio_id)
        .where(Prestamo.fecha_devolucion.is_(None))
        .where(Prestamo.fecha_limite < date.today())
    )
    if vencidos > 0:
        raise ReglaNegocio("El socio tiene préstamos vencidos")

    # R5: Menos de 3 préstamos sin devolver
    activos = db.scalar(
        select(func.count(Prestamo.id))
        .where(Prestamo.socio_id == datos.socio_id)
        .where(Prestamo.fecha_devolucion.is_(None))
    )
    if activos >= 3:
        raise ReglaNegocio("Máximo de 3 préstamos")

    # R6: No tiene el mismo libro prestado
    mismo_libro = db.scalar(
        select(func.count(Prestamo.id))
        .where(Prestamo.socio_id == datos.socio_id)
        .where(Prestamo.libro_id == datos.libro_id)
        .where(Prestamo.fecha_devolucion.is_(None))
    )
    if mismo_libro > 0:
        raise Conflicto("El socio ya tiene este libro prestado sin devolver")

    # R7: Ejemplares disponibles
    prestados_libro = db.scalar(
        select(func.count(Prestamo.id))
        .where(Prestamo.libro_id == datos.libro_id)
        .where(Prestamo.fecha_devolucion.is_(None))
    )
    if (libro.ejemplares - prestados_libro) <= 0:
        raise ReglaNegocio("No hay ejemplares disponibles")

    # R8: Cálculo de fecha límite
    f_prestamo = datos.fecha_prestamo or date.today()
    if f_prestamo > date.today():
        raise ReglaNegocio("La fecha de préstamo no puede ser futura")

    f_limite = f_prestamo + timedelta(days=datos.dias)

    nuevo_prestamo = Prestamo(
        libro_id=datos.libro_id,
        socio_id=datos.socio_id,
        fecha_prestamo=f_prestamo,
        fecha_limite=f_limite
    )
    db.add(nuevo_prestamo)
    db.commit()
    db.refresh(nuevo_prestamo)
    return nuevo_prestamo


def devolver_prestamo(db: Session, prestamo_id: int):
    # R9: Devolución
    prestamo = db.get(Prestamo, prestamo_id)
    if not prestamo:
        raise NoEncontrado("Préstamo no encontrado")
    if prestamo.fecha_devolucion is not None:
        raise Conflicto("El préstamo ya fue devuelto")

    hoy = date.today()
    prestamo.fecha_devolucion = hoy

    # R10: Cálculo de multa
    if hoy > prestamo.fecha_limite:
        dias_retraso = (hoy - prestamo.fecha_limite).days
        prestamo.multa = Decimal(dias_retraso) * Decimal("0.50")

    db.commit()
    db.refresh(prestamo)
    return prestamo
