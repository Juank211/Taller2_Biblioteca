from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class ErrorAplicacion(Exception):
    def __init__(self, status_code: int, detail: str, code: str = None):
        self.status_code = status_code
        self.detail = detail
        self.code = code

class LibrosSinCopiasException(ErrorAplicacion):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay copias disponibles de este libro",
            code="libros_sin_copias"
        )

class TokenRevocadoException(ErrorAplicacion):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revocado",
            code="token_revocado"
        )

class UsuarioNoEncontradoException(ErrorAplicacion):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
            code="usuario_no_encontrado"
        )

class CredencialesInvalidasException(ErrorAplicacion):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            code="credenciales_invalidas"
        )

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "code": exc.detail.lower().replace(" ", "_")
        }
    )

async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": "Error de validación",
            "errors": exc.errors(),
            "code": "validacion_error"
        }
    )

async def aplicacion_exception_handler(request: Request, exc: ErrorAplicacion):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "code": exc.code
        }
    )
    
class RecursoNoEncontrado(ErrorAplicacion):
    def __init__(self, detail: str = "Recurso no encontrado"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            code="recurso_no_encontrado"
        )
