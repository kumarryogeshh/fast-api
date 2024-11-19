"""
Model classes for the RPT schema.
Automatically maps all tables and their relationships.
"""

from typing import List
from sqlalchemy.ext.automap import automap_base
from app.models.base import Base, mapped_classes

# Export all mapped classes from RPT schema
Report = mapped_classes.get("Report")
# Add other related models as needed based on your database structure

__all__ = ["Report"] + list(mapped_classes.keys())
