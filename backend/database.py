"""Database setup and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# WHY: let deployments configure the DB without changing code
# WHAT: closes #config-db-url
# HOW: extend by using a PostgreSQL URI; roll back by hardcoding
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///pharma.db")

# Engine created for configured database (defaults to SQLite)
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Session factory for database operations
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def init_db():
    """Create tables based on ORM models."""
    from . import models  # Import models for metadata
    Base.metadata.create_all(bind=engine)
