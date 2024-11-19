"""
Database connection module.
Handles SQLAlchemy engine creation and session management.
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Connection string for Windows Authentication with schema specification
SQLALCHEMY_DATABASE_URL = (
    f"mssql+pyodbc://{settings.SQL_SERVER_HOST}/{settings.SQL_DATABASE}?"
    "driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,  # Enable pool pre-ping feature
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create MetaData instance with schema reflection
metadata = MetaData()

# Reflect all schemas
metadata.reflect(bind=engine, views=True, extend_existing=True)

# Create base class for models
Base = declarative_base(metadata=metadata)
