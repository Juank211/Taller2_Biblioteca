from fastapi import APIRouter, status
from app.core.dependencies import SessionDep, PaginacionDep
from app.schemas.prestamo import PrestamoOut, PrestamoCreate
from app.controllers import prestamo as controller

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])

@router.post("", response_model=PrestamoOut, status_code=status.HTTP_201_CREATED)
def crear_prestamo(datos: PrestamoCreate, db: SessionDep):
    return controller.crear_prestamo(db, datos)

@router.post("/{id}/devolucion", response_model=PrestamoOut)
def devolver_prestamo(id: int, db: SessionDep):
    return controller.devolver_prestamo(db, id)
