from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, ConfigDict

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Usuario, Libro, Prestamo
from app.schemas.libro import LibroResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

class AlertaItem(BaseModel):
    tipo: str  # "warning", "danger", "info", "success"
    titulo: str
    mensaje: str
    enlace: Optional[str] = None

class DashboardStatsOut(BaseModel):
    total_libros: int
    total_ejemplares_disponibles: int
    total_prestamos_activos: int
    total_usuarios: int
    es_admin: bool
    usuario_nombre: str
    usuario_rol: str

    prestamos_vencidos_total: int
    mis_prestamos_activos: int
    mis_prestamos_proximos_vencer: int
    mis_prestamos_vencidos: int

    alertas: List[AlertaItem]
    libros_recientes: List[LibroResponse]

    model_config = ConfigDict(from_attributes=True)

@router.get("/stats", response_model=DashboardStatsOut)
def obtener_estadisticas_dashboard(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    ahora = datetime.utcnow()
    total_libros = db.query(Libro).count()
    ejemplares = db.query(func.sum(Libro.copias_disponibles)).scalar() or 0
    total_usuarios = db.query(Usuario).count()

    prestamos_activos = db.query(Prestamo).filter(Prestamo.fecha_devuelto.is_(None)).all()
    total_prestamos_activos = len(prestamos_activos)

    prestamos_vencidos_total = 0
    for p in prestamos_activos:
        if p.fecha_prestamo:
            limite = p.fecha_prestamo + timedelta(days=14)
            if ahora > limite:
                prestamos_vencidos_total += 1

    # Préstamos del usuario actual
    mis_prestamos = [p for p in prestamos_activos if p.usuario_id == current_user.id]
    mis_prestamos_activos = len(mis_prestamos)
    mis_proximos = 0
    mis_vencidos = 0

    for p in mis_prestamos:
        if p.fecha_prestamo:
            limite = p.fecha_prestamo + timedelta(days=14)
            dias_restantes = (limite.date() - ahora.date()).days
            if dias_restantes < 0:
                mis_vencidos += 1
            elif dias_restantes <= 3:
                mis_proximos += 1

    alertas: List[AlertaItem] = []
    if mis_vencidos > 0:
        alertas.append(AlertaItem(
            tipo="danger",
            titulo="Préstamos Vencidos",
            mensaje=f"Tienes {mis_vencidos} libro(s) con fecha de devolución vencida. Por favor entrégalos para evitar multas adicionales.",
            enlace="/mis-prestamos"
        ))
    if mis_proximos > 0:
        alertas.append(AlertaItem(
            tipo="warning",
            titulo="Próximos a Vencer",
            mensaje=f"Tienes {mis_proximos} libro(s) que vencen en 3 días o menos.",
            enlace="/mis-prestamos"
        ))
    if current_user.rol == "admin" and prestamos_vencidos_total > 0:
        alertas.append(AlertaItem(
            tipo="danger",
            titulo="Préstamos Vencidos en la Biblioteca",
            mensaje=f"Hay {prestamos_vencidos_total} préstamo(s) activos vencidos pendientes de devolución.",
            enlace="/prestamos"
        ))

    libros_recientes = db.query(Libro).order_by(Libro.id.desc()).limit(8).all()

    return {
        "total_libros": total_libros,
        "total_ejemplares_disponibles": int(ejemplares),
        "total_prestamos_activos": total_prestamos_activos,
        "total_usuarios": total_usuarios,
        "es_admin": current_user.rol == "admin",
        "usuario_nombre": current_user.nombre,
        "usuario_rol": current_user.rol,
        "prestamos_vencidos_total": prestamos_vencidos_total,
        "mis_prestamos_activos": mis_prestamos_activos,
        "mis_prestamos_proximos_vencer": mis_proximos,
        "mis_prestamos_vencidos": mis_vencidos,
        "alertas": alertas,
        "libros_recientes": libros_recientes
    }
