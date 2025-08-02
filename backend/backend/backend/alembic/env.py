import os
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# ---------------------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------------------
cwd = Path.cwd()
if (cwd / ".env").exists():
    load_dotenv(cwd / ".env")
elif (cwd / "backend" / ".env").exists():
    load_dotenv(cwd / "backend" / ".env")
else:
    parent = cwd.parent
    if (parent / "backend" / ".env").exists():
        load_dotenv(parent / "backend" / ".env")
    else:
        print("WARNING: .env file not found in expected locations")

# ---------------------------------------------------------------------
# Alembic Config
# ---------------------------------------------------------------------
config = context.config

# Setup Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------
# Import your models and Base
# ---------------------------------------------------------------------
from app.database import Base  # Make sure app/database.py defines Base
from app import models  # Import models so metadata is populated

target_metadata = Base.metadata

# ---------------------------------------------------------------------
# Helper to get DB URL
# ---------------------------------------------------------------------
def get_url():
    env_url = os.getenv("SQLALCHEMY_DATABASE_URL")
    if env_url:
        return env_url
    # Default fallback (SQLite in backend folder)
    return "sqlite:///./survey.db"

# Override config sqlalchemy.url with env or fallback
db_url = get_url()
print(f"Alembic will connect to DB URL: {db_url}")
config.set_main_option("sqlalchemy.url", db_url)

# Ensure SQLite directory exists if using file-based SQLite
if db_url.startswith("sqlite:///"):
    db_path = Path(db_url.replace("sqlite:///", "", 1))
    if db_path.parent and not db_path.parent.exists():
        db_path.parent.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# Migration functions
# ---------------------------------------------------------------------
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
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
            compare_type=True,
            render_as_batch=True,  # Helpful for SQLite
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------------------
# Run Alembic
# ---------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
