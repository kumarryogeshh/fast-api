"""
Dependency injection module.
Contains reusable dependencies for FastAPI endpoints.
"""

from typing import Generator
from sqlalchemy.orm import Session
from app.core.database import SessionLocal


def get_db() -> Generator:
    """
    Dependency function to get database session.
    Yields a SQLAlchemy session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
