import io
import cloudinary.uploader
from cloudinary import CloudinaryImage

CARPETA_PORTADAS = "taller2_biblioteca/portadas"

def subir_portada_libro(contenido_bytes: bytes, libro_id: int) -> dict:
    """
    Suba la portada a Cloudinary usando public_id fijo para sobrescribir
    y evitar imágenes huérfanas en el almacenamiento.
    """
    resultado = cloudinary.uploader.upload(
        io.BytesIO(contenido_bytes),
        folder=CARPETA_PORTADAS,
        public_id=f"libro_{libro_id}",
        overwrite=True,
        invalidate=True,
        resource_type="image"
    )

    miniatura_url = CloudinaryImage(resultado["public_id"]).build_url(
        width=200,
        height=300,
        crop="fill",
        fetch_format="auto",
        quality="auto"
    )

    return {
        "portada_url": resultado["secure_url"],
        "portada_public_id": resultado["public_id"],
        "miniatura_url": miniatura_url,
        "formato": resultado["format"],
        "ancho": resultado["width"],
        "alto": resultado["height"],
        "bytes": resultado["bytes"]
    }

def eliminar_portada_libro(public_id: str):
    """Elimina la portada de Cloudinary si existe."""
    if public_id:
        cloudinary.uploader.destroy(public_id, invalidate=True)
