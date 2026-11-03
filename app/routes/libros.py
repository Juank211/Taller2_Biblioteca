from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, get_current_active_admin
from app.models import Libro, Usuario
from app.schemas import LibroCreate, LibroUpdate, LibroResponse
from app.services.libro_service import LibroService

router = APIRouter(prefix="/api/v1/libros", tags=["Libros"])

@router.post("/", response_model=LibroResponse, status_code=status.HTTP_201_CREATED)
def crear_libro(
    libro: LibroCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_active_admin)
):
    return LibroService.crear_libro(db, libro)

@router.get("/", response_model=List[LibroResponse])
def listar_libros(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(Libro).all()

@router.get("/{libro_id}", response_model=LibroResponse)
def leer_libro(
    libro_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return LibroService.obtener_libro(db, libro_id)

@router.put("/{libro_id}", response_model=LibroResponse)
def actualizar_libro(
    libro_id: int,
    libro: LibroUpdate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_active_admin)
):
    return LibroService.actualizar_libro(db, libro_id, libro)

@router.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(
    libro_id: int,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_active_admin)
):
    LibroService.eliminar_libro(db, libro_id)
    return None
