"""
API router module.
Contains all API endpoint definitions.
"""

from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.report import Report
from app.schemas.base import ResponseSchema
from app.utils.db_utils import get_schema_tables, get_table_columns

router = APIRouter()


@router.get("/health")
def health_check() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Dict[str, str]: Health status
    """
    return {"status": "healthy"}


@router.get("/schemas")
def get_schemas_and_tables() -> ResponseSchema[Dict[str, List[str]]]:
    """
    Get all schemas and their tables in the database.

    Returns:
        ResponseSchema[Dict[str, List[str]]]: Dictionary of schemas and their tables
    """
    try:
        schema_tables = get_schema_tables()
        return ResponseSchema(
            success=True,
            message="Schemas and tables retrieved successfully",
            data=schema_tables,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schemas/{schema}/tables/{table}/columns")
def get_table_structure(schema: str, table: str) -> ResponseSchema[List[Dict]]:
    """
    Get column information for a specific table.

    Args:
        schema (str): Schema name
        table (str): Table name

    Returns:
        ResponseSchema[List[Dict]]: List of column information
    """
    try:
        columns = get_table_columns(schema, table)
        return ResponseSchema(
            success=True,
            message=f"Column information retrieved for {schema}.{table}",
            data=columns,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports")
def get_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
) -> ResponseSchema[List[Any]]:
    """
    Get records from the Report table.

    Args:
        skip (int): Number of records to skip
        limit (int): Maximum number of records to return
        db (Session): Database session from dependency

    Returns:
        ResponseSchema[List[Any]]: List of Report records
    """
    try:
        reports = db.query(Report).offset(skip).limit(limit).all()
        return ResponseSchema(
            success=True, message="Reports retrieved successfully", data=reports
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
