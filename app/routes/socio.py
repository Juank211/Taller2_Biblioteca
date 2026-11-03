from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.socio import Socio
from app.schemas.socio import SocioIn, SocioOut
from fastapi import HTTPException
from app.core.exceptions import RecursoNoEncontrado, Conflicto

router = APIRouter(prefix="/socios", tags=["Socios"])

@router.post("", response_model=SocioOut, status_code=status.HTTP_201_CREATED)
def crear_socio(datos: SocioIn, db: Session = Depends(get_db)):
    existente = db.scalar(select(Socio).where(Socio.email == datos.email))
    if existente:
        raise Conflicto("Ya existe un socio con este email")
    socio = Socio(**datos.model_dump())
    db.add(socio)
    db.commit()
    db.refresh(socio)
    return socio

@router.get("", response_model=list[SocioOut])
def listar_socios(db: Session = Depends(get_db)):
    return db.scalars(select(Socio).order_by(Socio.id)).all()

@router.get("/{socio_id}", response_model=SocioOut)
def obtener_socio(socio_id: int, db: Session = Depends(get_db)):
    socio = db.get(Socio, socio_id)
    if not socio:
        raise RecursoNoEncontrado("Socio no encontrado")
    return socio
