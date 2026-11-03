# Directrices del Proyecto: Biblioteca Segura (FastAPI)

## 1. Stack Tecnológico & Entorno
* **Framework:** FastAPI con Python 3.12+
* **Base de Datos & ORM:** PostgreSQL con SQLAlchemy y Alembic para migraciones.
* **Autenticación:** Seguridad JWT y control de acceso RBAC.
* **Entorno Virtual:** `venv` (ubicado en la raíz local).

## 2. Estándares de Código y Arquitectura
* Mantén una estructura modular separando rutas (`routers/`), modelos (`models/`), esquemas Pydantic (`schemas/`), y lógica de negocio (`services/` o `crud/`).
* Tipado estricto con Python type hints en todas las funciones y endpoints.
* Las consultas a la base de datos deben usar la sesión inyectada por dependencia (`SessionDep` / `get_db`).

## 3. Comandos Útiles del Proyecto
* **Activar entorno virtual:** `source venv/bin/activate`
* **Ejecutar servidor local:** `uvicorn app.main:app --reload`
* **Aplicar migraciones de Alembic:** `alembic upgrade head`
* **Crear nueva migración:** `alembic revision --autogenerate -m "descripción"`
* **Ejecutar pruebas:** `pytest`

## 4. Restricciones Importantes
* No incluyas credenciales reales ni claves secretas en el código; usa siempre el archivo `.env`.
* No modifiques migraciones de Alembic que ya hayan sido aplicadas en producción o en la base de datos principal sin un respaldo previo.