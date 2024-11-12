"""
API router module.
Contains all API endpoint definitions.
"""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.base import Base
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


@router.get("/tables")
def get_tables(db: Session = Depends(get_db)) -> ResponseSchema[List[str]]:
    """
    Get all available tables in the database.

    Args:
        db (Session): Database session from dependency

    Returns:
        ResponseSchema[List[str]]: List of table names
    """
    try:
        tables = Base.classes.keys()
        return ResponseSchema(
            success=True, message="Tables retrieved successfully", data=list(tables)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tables/{table_name}/records")
def get_table_records(
    table_name: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
) -> ResponseSchema[List[Any]]:
    """
    Get records from a specific table.

    Args:
        table_name (str): Name of the table
        skip (int): Number of records to skip
        limit (int): Maximum number of records to return
        db (Session): Database session from dependency

    Returns:
        ResponseSchema[List[Any]]: List of records from the table
    """
    try:
        if table_name not in Base.classes:
            raise HTTPException(
                status_code=404, detail=f"Table '{table_name}' not found"
            )

        Table = Base.classes[table_name]
        records = db.query(Table).offset(skip).limit(limit).all()

        return ResponseSchema(
            success=True,
            message=f"Records retrieved successfully from {table_name}",
            data=records,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
