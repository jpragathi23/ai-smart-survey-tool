import sys
import os
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# ---------------------------------------------------------------------
# Ensure project root / backend is importable so "app" package resolves.
# Assumes this file lives in something like <repo>/backend/alembic/env.py
# Adjust if your layout differs.
# ---------------------------------------------------------------------
current_file = Path(__file__).resolve()
# If env.py is in backend/alembic/, parent[1] is backend; add repo root if needed:
sys.path.append(str(current_file.parents[2]))  # repo root
sys.path.append(str(current_file.parents[1]))  # backend (where `app` likely lives)

# ---------------------------------------------------------------------
# Load .env (prefer project root, fallback to backend/)
# ---------------------------------------------------------------------
project_root = current_file.parents[2]
backend_dir = current_file.parents[1]
env_paths = [project_root / ".env", backend_dir / ".env"]
for p in env_paths:
    if p.exists():
        load_dotenv(p)
        break

# ---------------------------------------------------------------------
# Alembic config & logging
# ---------------------------------------------------------------------
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------
# Import your metadata so autogenerate can work.
# Adjust the import path if your package structure is different.
# ---------------------------------------------------------------------
from app.database import Base  # must expose SQLAlchemy declarative Base
# importing model modules so they register with metadata if needed
import app.models.survey  # noqa: F401
import app.models.user  # noqa: F401
import app.models.question  # noqa: F401
import app.models.response  # noqa: F401
import app.models.enumerator  # noqa: F401

target_metadata = Base.metadata

# ---------------------------------------------------------------------
# Database URL resolution
# ---------------------------------------------------------------------
def get_database_url():
    # env var takes precedence
    env_url = os.getenv("SQLALCHEMY_DATABASE_URL")
    if env_url:
        return env_url
    # fallback to alembic.ini value if already set there
    ini_url = config.get_main_option("sqlalchemy.url")
    if ini_url:
        return ini_url
    # last-resort default
    return "sqlite:///./survey.db"


# Override config if env supplies it
db_url = get_database_url()
config.set_main_option("sqlalchemy.url", db_url)

# If using file-based SQLite, ensure directory exists
if db_url.startswith("sqlite:///"):
    # strip prefix and handle relative path
    raw_path = db_url.replace("sqlite:///", "", 1)
    db_path = Path(raw_path)
    if not db_path.is_absolute():
        db_path = (Path.cwd() / db_path).resolve()
    parent = db_path.parent
    if parent and not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# Migration runners
# ---------------------------------------------------------------------
def run_migrations_offline() -> None:
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        render_as_batch=True if url.startswith("sqlite:///") else False,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        is_sqlite = db_url.lower().startswith("sqlite:///")
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            render_as_batch=True if is_sqlite else False,
        )
        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------------------
# Execute
# ---------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
