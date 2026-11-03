from datetime import datetime
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Usuario, Prestamo
from app.schemas import PrestamoCreate, PrestamoResponse
from app.services.prestamo_service import PrestamoService

router = APIRouter(prefix="/api/v1/prestamos", tags=["Prestamos"])

@router.post("/", response_model=PrestamoResponse, status_code=status.HTTP_201_CREATED)
def solicitar_prestamo(
    prestamo: PrestamoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return PrestamoService.crear_prestamo(db, prestamo, current_user.id)

@router.put("/{prestamo_id}/devolver", response_model=PrestamoResponse)
def devolver_prestamo(
    prestamo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return PrestamoService.devolver_prestamo(db, prestamo_id, datetime.utcnow())
