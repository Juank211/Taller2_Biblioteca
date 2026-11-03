from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, get_current_active_admin
from app.models import Usuario
from app.schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"])

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_active_admin)
):
    return UsuarioService.crear_usuario(db, usuario)

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_active_admin)
):
    return db.query(Usuario).all()

@router.get("/me", response_model=UsuarioResponse)
def leer_perfil_mio(
    current_user: Usuario = Depends(get_current_user)
):
    return current_user

@router.put("/me", response_model=UsuarioResponse)
def actualizar_perfil_mio(
    usuario: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return UsuarioService.actualizar_usuario(db, current_user.id, usuario)

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_active_admin)
):
    UsuarioService.eliminar_usuario(db, usuario_id)
    return None
