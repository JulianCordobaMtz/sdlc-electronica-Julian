import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# Importar `Base` para registrar la metadata
from app.db import Base

# Importar modelos para que Alembic detecte todas las tablas.
from app.models.alert import AlertModel  # noqa: F401, E402
from app.models.reading import ReadingModel  # noqa: F401, E402
from app.models.sensor import SensorModel  # noqa: F401, E402

# Objeto de configuración de Alembic [3]
config = context.config

# Configuración de logs estándar [4]
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------
# CONFIGURACIÓN DINÁMICA DE LA BASE DE DATOS (Local vs Render) [5, 6]
# ---------------------------------------------------------------------
database_url = os.getenv("DATABASE_URL")

if database_url:
    # Render puede entregar postgres://, pero SQLAlchemy 2.0 exige postgresql:// [6]
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    # Forzamos el uso del driver psycopg que agregamos a requirements.txt [5]
    if "postgresql://" in database_url and "+psycopg" not in database_url:
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    # Inyectamos la URL de producción dinámicamente en Alembic [7]
    config.set_main_option("sqlalchemy.url", database_url)
else:
    # Respaldo local de SQLite si no estamos en Render [5]
    config.set_main_option("sqlalchemy.url", "sqlite:///sensorhub.db")
# ---------------------------------------------------------------------

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecutar migraciones en modo 'online'."""
    configuration = config.get_section(config.config_ini_section, {})
    url = config.get_main_option("sqlalchemy.url")

    # Evitar bloqueos de hilos en pruebas de desarrollo local con SQLite [5]
    connect_args = {}
    if url and url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
