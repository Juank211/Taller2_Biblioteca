import sys
import os
from logging.config import fileConfig
from alembic import context

# Add the project root directory to the system path
sys.path.append(os.getcwd())

# Usa el MISMO engine que la app (lee DATABASE_URL del .env o del entorno),
# en lugar de la URL fija de alembic.ini. Asi Alembic y la API siempre
# apuntan a la misma base de datos.
from app.core.database import Base, engine
import app.models  # noqa: F401  (registra los modelos en Base.metadata)
from app.models import autor, socio  # noqa: F401

target_metadata = Base.metadata

config = context.config
fileConfig(config.config_file_name)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
