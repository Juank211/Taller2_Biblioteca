from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Prestamo, Libro, Multa, Usuario
from app.schemas.prestamo import PrestamoCreate
from app.core.exceptions import ErrorAplicacion, RecursoNoEncontrado

class PrestamoService:
    @staticmethod
    def crear_prestamo(db: Session, prestamo: PrestamoCreate, usuario_id: int) -> Prestamo:
        libro = db.query(Libro).filter(Libro.id == prestamo.libro_id).first()
        if not libro:
            raise RecursoNoEncontrado("Libro no encontrado")

        if libro.copias_disponibles <= 0:
            raise ErrorAplicacion(
                status_code=400,
                detail="No hay copias disponibles de este libro"
            )

        libro.copias_disponibles -= 1
        if libro.copias_disponibles == 0:
            libro.estado = "Agotado"
        db.add(libro)

        prestamo_db = Prestamo(
            usuario_id=usuario_id,
            libro_id=prestamo.libro_id,
            estado=prestamo.estado or "Activo"
        )
        db.add(prestamo_db)
        db.commit()
        db.refresh(prestamo_db)
        return prestamo_db

    @staticmethod
    def devolver_prestamo(db: Session, prestamo_id: int, fecha_devuelto: datetime, current_user: Optional[Usuario] = None) -> Prestamo:
        prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
        if not prestamo:
            raise RecursoNoEncontrado("Préstamo no encontrado")

        if current_user and current_user.rol != "admin" and prestamo.usuario_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para devolver este préstamo"
            )

        if prestamo.fecha_devuelto is not None:
            raise ErrorAplicacion(
                status_code=400,
                detail="Este préstamo ya ha sido devuelto anteriormente"
            )

        libro = db.query(Libro).filter(Libro.id == prestamo.libro_id).first()
        if libro:
            libro.copias_disponibles += 1
            if libro.estado == "Agotado":
                libro.estado = "Disponible"
            db.add(libro)

        prestamo.fecha_devuelto = fecha_devuelto
        prestamo.estado = "Devuelto"
        db.commit()
        db.refresh(prestamo)

        # Regla de negocio: Préstamo vence a los 14 días
        if prestamo.fecha_devuelto and prestamo.fecha_prestamo:
            dias_totales = (prestamo.fecha_devuelto.date() - prestamo.fecha_prestamo.date()).days
            if dias_totales > 14:
                dias_retraso = dias_totales - 14
                monto_multa = float(dias_retraso * 1000)
                multa = Multa(
                    usuario_id=prestamo.usuario_id,
                    prestamo_id=prestamo.id,
                    monto=monto_multa,
                    pagado=False
                )
                db.add(multa)
                db.commit()

        return prestamo

    @staticmethod
    def listar_prestamos(db: Session, usuario_id: Optional[int] = None, solo_activos: bool = False):
        query = db.query(Prestamo)
        if usuario_id is not None:
            query = query.filter(Prestamo.usuario_id == usuario_id)
        if solo_activos:
            query = query.filter(Prestamo.fecha_devuelto.is_(None))

        prestamos = query.order_by(Prestamo.fecha_prestamo.desc()).all()

        ahora = datetime.utcnow()
        resultado = []
        for p in prestamos:
            fecha_limite = p.fecha_prestamo + timedelta(days=14) if p.fecha_prestamo else ahora + timedelta(days=14)
            if p.fecha_devuelto:
                dias_restantes = 0
                vencido = p.fecha_devuelto > fecha_limite
                dias_retraso = max(0, (p.fecha_devuelto.date() - p.fecha_prestamo.date()).days - 14) if p.fecha_prestamo else 0
                multa_estimada = float(dias_retraso * 1000)
            else:
                dias_restantes = (fecha_limite.date() - ahora.date()).days
                vencido = dias_restantes < 0
                dias_retraso = max(0, -dias_restantes)
                multa_estimada = float(dias_retraso * 1000)

            resultado.append({
                "id": p.id,
                "libro_id": p.libro_id,
                "libro_titulo": p.libro.titulo if p.libro else "Libro no identificado",
                "libro_autor": p.libro.autor if p.libro else "Desconocido",
                "libro_portada_url": p.libro.portada_url if p.libro else None,
                "usuario_id": p.usuario_id,
                "usuario_nombre": p.usuario.nombre if p.usuario else "Usuario",
                "usuario_email": p.usuario.email if p.usuario else "",
                "fecha_prestamo": p.fecha_prestamo or ahora,
                "fecha_limite": fecha_limite,
                "fecha_devuelto": p.fecha_devuelto,
                "estado": p.estado,
                "dias_restantes": dias_restantes,
                "vencido": vencido,
                "dias_retraso": dias_retraso,
                "multa_estimada": multa_estimada
            })
        return resultado
