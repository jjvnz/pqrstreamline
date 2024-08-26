from __future__ import annotations
import sys
from pathlib import Path
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.declarative import DeclarativeMeta
from alembic import context
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

# Configuración del proyecto
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Obtener la URL de la base de datos desde la variable de entorno
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Importa Base aquí
from app.database import Base

# Importa los modelos después de definir Base
from app.models import Request

target_metadata: DeclarativeMeta = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
