from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.autor import Autor
from app.schemas.autor import AutorIn, AutorOut
from app.core.exceptions import RecursoNoEncontrado

router = APIRouter(prefix="/autores", tags=["Autores"])

@router.post("", response_model=AutorOut, status_code=status.HTTP_201_CREATED)
def crear_autor(datos: AutorIn, db: Session = Depends(get_db)):
    autor = Autor(**datos.model_dump())
    db.add(autor)
    db.commit()
    db.refresh(autor)
    return autor

@router.get("", response_model=list[AutorOut])
def listar_autores(db: Session = Depends(get_db)):
    return db.scalars(select(Autor).order_by(Autor.id)).all()

@router.get("/{autor_id}", response_model=AutorOut)
def obtener_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = db.get(Autor, autor_id)
    if not autor:
        raise RecursoNoEncontrado("Autor no encontrado")
    return autor
