"""Database setup and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///pharma.db"

# Engine created for SQLite database
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Session factory for database operations
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def init_db():
    """Create tables based on ORM models."""
    from . import models  # Import models for metadata
    Base.metadata.create_all(bind=engine)
