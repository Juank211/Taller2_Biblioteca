from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user, get_current_active_admin
from app.models import Usuario
from app.schemas import LoginSchema, TokenResponse, TokenData, UsuarioCreate, UsuarioResponse
from app.core.security import get_current_user, get_current_active_admin, oauth2_scheme
from app.services.auth_service import (
    obtener_password_hash,
    verificar_password,
    crear_access_token,
    crear_refresh_token,
    revocar_token,
)
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    # Verificar si el usuario ya existe
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Solo el primer usuario registrado es admin; los demás siempre son "usuario"
    rol = "admin" if db.query(Usuario).count() == 0 else "usuario"

    db_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password_hash=obtener_password_hash(usuario.password),
        rol=rol,
        activo=True
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not usuario or not verificar_password(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = crear_access_token(
        data={"sub": usuario.email}
    )
    refresh_token = crear_refresh_token(
        data={"sub": usuario.email}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(refresh_token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise credentials_exception

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = crear_access_token(
        data={"sub": usuario.email, "jti": str(usuario.id)}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(
    token: str = Depends(oauth2_scheme),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Revocar solo el token que se está usando
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    expiracion = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    revocar_token(db, payload["jti"], expiracion)
    return {"detail": "Sesión cerrada exitosamente"}

@router.put("/{usuario_id}/rol", response_model=UsuarioResponse)
def actualizar_rol(
    usuario_id: int,
    rol: str,
    current_user: Usuario = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    if rol not in ("admin", "usuario"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rol no válido"
        )

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    usuario.rol = rol
    db.commit()
    db.refresh(usuario)
    return usuario
