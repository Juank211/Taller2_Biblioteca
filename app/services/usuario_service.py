from sqlalchemy.orm import Session
from app.models import Usuario
from app.schemas import UsuarioCreate, UsuarioUpdate
from app.services.auth_service import obtener_password_hash, verificar_password
from fastapi import HTTPException
from app.core.exceptions import ErrorAplicacion

class UsuarioService:
    @staticmethod
    def crear_usuario(db: Session, usuario: UsuarioCreate) -> Usuario:
        db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
        if db_usuario:
            raise ErrorAplicacion(
                status_code=400,
                detail="El email ya está registrado"
            )

        hashed_password = obtener_password_hash(usuario.password)
        db_usuario = Usuario(
            nombre=usuario.nombre,
            email=usuario.email,
            password_hash=hashed_password,
            rol=usuario.rol,
            activo=usuario.activo
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def obtener_usuario(db: Session, usuario_id: int) -> Usuario:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise ErrorAplicacion(
                status_code=404,
                detail="Usuario no encontrado"
            )
        return usuario

    @staticmethod
    def actualizar_usuario(db: Session, usuario_id: int, usuario: UsuarioUpdate) -> Usuario:
        db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not db_usuario:
            raise ErrorAplicacion(
                status_code=404,
                detail="Usuario no encontrado"
            )

        if usuario.nombre:
            db_usuario.nombre = usuario.nombre
        if usuario.email:
            db_usuario.email = usuario.email
        if usuario.password:
            db_usuario.password_hash = obtener_password_hash(usuario.password)
        if usuario.rol:
            db_usuario.rol = usuario.rol
        if usuario.activo is not None:
            db_usuario.activo = usuario.activo

        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def eliminar_usuario(db: Session, usuario_id: int) -> None:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise ErrorAplicacion(
                status_code=404,
                detail="Usuario no encontrado"
            )
        db.delete(usuario)
        db.commit()
