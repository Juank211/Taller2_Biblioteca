from typing import Annotated
from fastapi import Query, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

class Paginacion:
    def __init__(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
    ):
        self.skip = skip
        self.limit = limit

SessionDep = Annotated[Session, Depends(get_db)]
PaginacionDep = Annotated[Paginacion, Depends()]
