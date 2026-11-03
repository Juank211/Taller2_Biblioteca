from sqlalchemy.orm import Session
from app.models import Multa
from app.core.exceptions import ErrorAplicacion, RecursoNoEncontrado

class MultaService:
    @staticmethod
    def pagar_multa(db: Session, multa_id: int) -> Multa:
        multa = db.query(Multa).filter(Multa.id == multa_id).first()
        if not multa:
            raise RecursoNoEncontrado("Multa no encontrada")

        multa.pagado = True
        db.commit()
        db.refresh(multa)
        return multa

    @staticmethod
    def obtener_multas(db: Session, usuario_id: int) -> list:
        return db.query(Multa).filter(Multa.usuario_id == usuario_id).all()
