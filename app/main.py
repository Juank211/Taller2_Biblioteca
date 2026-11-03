from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, HTTPException

from app.core.database import Base, engine
from app.core.exceptions import (
    ErrorAplicacion,
    http_exception_handler,
    request_validation_exception_handler,
    aplicacion_exception_handler
)
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.routes import auth, usuarios, libros, prestamos, multas, health

# Configuración de logging
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear las tablas al iniciar la aplicación
    import app.models  # noqa
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Taller API FastAPI Biblioteca",
    version="1.0.0",
    lifespan=lifespan
)

# Exception Handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(ErrorAplicacion, aplicacion_exception_handler)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")
app.include_router(libros.router, prefix="/api/v1")
app.include_router(prestamos.router, prefix="/api/v1")
app.include_router(multas.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")
