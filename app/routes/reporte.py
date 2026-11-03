from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.prestamo import Prestamo
from app.models.socio import Socio
from app.models.libro import Libro

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/estadisticas")
def obtener_estadisticas(db: Session = Depends(get_db)):
    total_libros = db.scalar(select(func.count(Libro.id))) or 0
    total_socios = db.scalar(select(func.count(Socio.id))) or 0
    prestamos_activos = db.scalar(
        select(func.count(Prestamo.id)).where(Prestamo.fecha_devolucion.is_(None))
    ) or 0
    total_multas = db.scalar(select(func.sum(Prestamo.multa))) or 0.0

    return {
        "total_libros": total_libros,
        "total_socios": total_socios,
        "prestamos_activos": prestamos_activos,
        "total_multas_acumuladas": float(total_multas),
    }
