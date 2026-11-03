from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Usuario
from app.schemas import MultaResponse
from app.services.multa_service import MultaService

router = APIRouter(prefix="/api/v1/multas", tags=["Multas"])

@router.get("/", response_model=List[MultaResponse])
def consultar_multas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return MultaService.obtener_multas(db, current_user.id)

@router.post("/{multa_id}/pagar", response_model=MultaResponse)
def pagar_multa(
    multa_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return MultaService.pagar_multa(db, multa_id)
