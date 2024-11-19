"""
API router module for Report CRUD operations.
"""

from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.report import report
from app.schemas.base import ResponseSchema

router = APIRouter()


@router.get("/health")
def health_check() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Dict[str, str]: Health status
    """
    return {"status": "healthy"}


@router.get("/reports")
def get_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    filters: Dict[str, Any] = None,
    db: Session = Depends(get_db),
) -> ResponseSchema[List[Any]]:
    """
    Get reports with optional filtering.
    """
    try:
        reports = report.get_by_filters(db, filters, skip=skip, limit=limit)
        return ResponseSchema(
            success=True, message="Reports retrieved successfully", data=reports
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reports")
def create_report(
    report_data: Dict[str, Any], db: Session = Depends(get_db)
) -> ResponseSchema[Any]:
    """
    Create a new report.
    """
    try:
        new_report = report.create_with_relations(db, report_data)
        return ResponseSchema(
            success=True, message="Report created successfully", data=new_report
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/reports/{report_id}")
def update_report(
    report_id: int, report_data: Dict[str, Any], db: Session = Depends(get_db)
) -> ResponseSchema[Any]:
    """
    Update an existing report.
    """
    try:
        db_report = report.get(db, report_id)
        if not db_report:
            raise HTTPException(status_code=404, detail="Report not found")

        updated_report = report.update_with_relations(db, db_report, report_data)
        return ResponseSchema(
            success=True, message="Report updated successfully", data=updated_report
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/reports/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)) -> ResponseSchema[Any]:
    """
    Delete a report.
    """
    try:
        db_report = report.get(db, report_id)
        if not db_report:
            raise HTTPException(status_code=404, detail="Report not found")

        db.delete(db_report)
        db.commit()
        return ResponseSchema(
            success=True, message="Report deleted successfully", data=None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
