from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaIn, CategoriaOut
from app.core.exceptions import RecursoNoEncontrado

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.post("", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED)
def crear_categoria(datos: CategoriaIn, db: Session = Depends(get_db)):
    categoria = Categoria(**datos.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

@router.get("", response_model=list[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return db.scalars(select(Categoria).order_by(Categoria.id)).all()

@router.get("/{categoria_id}", response_model=CategoriaOut)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    cat = db.get(Categoria, categoria_id)
    if not cat:
        raise RecursoNoEncontrado("Categoría no encontrada")
    return cat
