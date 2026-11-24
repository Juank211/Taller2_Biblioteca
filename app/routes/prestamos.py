from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Usuario
from app.schemas.prestamo import PrestamoCreate, PrestamoOut, PrestamoDetalleOut
from app.services.prestamo_service import PrestamoService

router = APIRouter(prefix="/prestamos", tags=["Prestamos"])

@router.get("/", response_model=List[PrestamoDetalleOut])
def listar_prestamos(
    solo_activos: bool = False,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Si es admin, puede ver todos los préstamos. Si es lector común, solo ve los suyos.
    usuario_id = None if current_user.rol == "admin" else current_user.id
    return PrestamoService.listar_prestamos(db, usuario_id=usuario_id, solo_activos=solo_activos)

@router.get("/mis-prestamos", response_model=List[PrestamoDetalleOut])
def mis_prestamos(
    solo_activos: bool = False,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return PrestamoService.listar_prestamos(db, usuario_id=current_user.id, solo_activos=solo_activos)

@router.post("/", response_model=PrestamoOut, status_code=status.HTTP_201_CREATED)
def solicitar_prestamo(
    prestamo: PrestamoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    usuario_id = prestamo.usuario_id if (current_user.rol == "admin" and prestamo.usuario_id) else current_user.id
    return PrestamoService.crear_prestamo(db, prestamo, usuario_id)

@router.put("/{prestamo_id}/devolver", response_model=PrestamoOut)
def devolver_prestamo(
    prestamo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return PrestamoService.devolver_prestamo(db, prestamo_id, datetime.utcnow(), current_user=current_user)
