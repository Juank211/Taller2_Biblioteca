from typing import List
from fastapi import APIRouter, Depends, status, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, get_current_active_admin
from app.models import Libro, Usuario
from app.schemas import LibroCreate, LibroUpdate, LibroResponse
from app.services.libro_service import LibroService
from app.services.cloudinary_service import subir_portada_libro

router = APIRouter(prefix="/api/v1/libros", tags=["Libros"])

@router.post("/{libro_id}/portada", response_model=dict)
async def subir_portada(
    libro_id: int,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: Usuario = Depends(get_current_active_admin)
):
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado"
        )

    if archivo.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato inválido. Solo se admiten imágenes JPG, PNG o WEBP"
        )

    contenido = await archivo.read()

    datos_portada = subir_portada_libro(contenido, libro_id)

    libro.portada_url = datos_portada["portada_url"]
    libro.portada_public_id = datos_portada["portada_public_id"]
    db.commit()
    db.refresh(libro)

    return {
        "mensaje": "Portada subida exitosamente",
        "libro_id": libro.id,
        "nombre_original": archivo.filename,
        **datos_portada
    }

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
