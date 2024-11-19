"""
CRUD operations for Report model.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.report import Report
from app.crud.base import CRUDBase


class CRUDReport(CRUDBase[Report]):
    """
    CRUD operations for Report model with additional specific methods.
    """

    def get_by_filters(
        self, db: Session, filters: Dict[str, Any], skip: int = 0, limit: int = 100
    ) -> List[Report]:
        """
        Get reports by multiple filters.

        Args:
            db (Session): Database session
            filters (Dict[str, Any]): Dictionary of filter conditions
            skip (int): Number of records to skip
            limit (int): Maximum number of records to return

        Returns:
            List[Report]: List of filtered reports
        """
        query = db.query(self.model)

        # Apply filters dynamically based on Report columns
        if filters:
            filter_conditions = []
            for key, value in filters.items():
                if hasattr(self.model, key):
                    filter_conditions.append(getattr(self.model, key) == value)
            if filter_conditions:
                query = query.filter(and_(*filter_conditions))

        return query.offset(skip).limit(limit).all()

    def create_with_relations(self, db: Session, obj_in: Dict[str, Any]) -> Report:
        """
        Create a new report with related data.

        Args:
            db (Session): Database session
            obj_in (Dict[str, Any]): Report data including related objects

        Returns:
            Report: Created report instance
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_with_relations(
        self, db: Session, db_obj: Report, obj_in: Dict[str, Any]
    ) -> Report:
        """
        Update a report and its relations.

        Args:
            db (Session): Database session
            db_obj (Report): Existing report instance
            obj_in (Dict[str, Any]): Updated report data

        Returns:
            Report: Updated report instance
        """
        for field in obj_in:
            if hasattr(db_obj, field):
                setattr(db_obj, field, obj_in[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


# Create CRUD instance
report = CRUDReport(Report)
