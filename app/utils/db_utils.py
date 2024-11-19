"""
Database utility functions.
"""

from typing import Dict, List
from sqlalchemy import inspect
from app.core.database import engine


def get_schema_tables() -> Dict[str, List[str]]:
    """
    Get all schemas and their tables from the database.

    Returns:
        Dict[str, List[str]]: Dictionary with schema names as keys and list of tables as values
    """
    inspector = inspect(engine)
    schemas = inspector.get_schema_names()

    schema_tables = {}
    for schema in schemas:
        tables = inspector.get_table_names(schema=schema)
        schema_tables[schema] = tables

    return schema_tables


def get_table_columns(schema: str, table: str) -> List[Dict]:
    """
    Get column information for a specific table.

    Args:
        schema (str): Schema name
        table (str): Table name

    Returns:
        List[Dict]: List of column information dictionaries
    """
    inspector = inspect(engine)
    return inspector.get_columns(table_name=table, schema=schema)
