"""
Base models module.
Handles database reflection and model creation using SQLAlchemy automap.
"""

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
from app.core.database import engine

# Create MetaData instance for RPT schema
metadata = MetaData(schema="RPT")

# Create automap base
Base = automap_base(metadata=metadata)

# Reflect the database schema with relationships
Base.prepare(
    engine,
    reflect=True,
    schema="RPT",
    name_for_scalar_relationship=lambda base, local_cls, referred_cls, constraint: f"{referred_cls.__name__.lower()}_ref",
    name_for_collection_relationship=lambda base, local_cls, referred_cls, constraint: f"{referred_cls.__name__.lower()}_collection",
)

# Get all mapped classes from RPT schema
mapped_classes = {
    name: cls for name, cls in Base.classes.items() if cls.__table__.schema == "RPT"
}
