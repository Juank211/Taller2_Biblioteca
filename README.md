# Taller 2: Biblioteca Segura

API REST desarrollada con FastAPI para la gestión de una biblioteca, implementando seguridad JWT, control de acceso RBAC y manejo de migraciones con Alembic.

## Requisitos Previos
- Python 3.12+
- Docker y Docker Compose
- PostgreSQL

## Configuración
1. Clonar el repositorio.
2. Crear un archivo `.env` basado en `.env.example`:
   ```bash
   DATABASE_URL=postgresql+psycopg://postgres:1234@localhost:5432/biblioteca_db
   TEST_DATABASE_URL=postgresql+psycopg://postgres:1234@localhost:5432/test_db
   SECRET_KEY=tu_secreto
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   CORS_ORIGINS=["http://localhost:3000"]
   ENVIRONMENT=development
   ```

## Ejecución Local
1. Crear entorno virtual: `python -m venv venv`
2. Activar: `source venv/bin/activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Aplicar migraciones: `alembic upgrade head`
5. Ejecutar servidor: `uvicorn app.main:app --reload`

## Despliegue con Docker
Para levantar la base de datos y el backend:
```bash
docker-compose up --build
```

## Pruebas
Para ejecutar la suite de pruebas automatizadas:
```bash
pytest
```
