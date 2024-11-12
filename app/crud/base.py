"""
Base CRUD operations module.
Contains generic CRUD operations that can be used with any model.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.orm import Session
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    """
    Base class for CRUD operations.
    Provides generic Create, Read, Update, Delete operations.
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUD object with SQLAlchemy model.

        Args:
            model (Type[ModelType]): SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID.

        Args:
            db (Session): Database session
            id (Any): Record ID

        Returns:
            Optional[ModelType]: Found record or None
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.

        Args:
            db (Session): Database session
            skip (int): Number of records to skip
            limit (int): Maximum number of records to return

        Returns:
            List[ModelType]: List of found records
        """
        return db.query(self.model).offset(skip).limit(limit).all()
