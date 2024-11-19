"""
Model class for the Report table in RPT schema.
"""

from sqlalchemy.ext.automap import automap_base
from app.core.database import Base, engine

# Create automap base
AutomapBase = automap_base()

# Prepare the automap base
AutomapBase.prepare(engine, reflect=True, schema=None)  # This will reflect all schemas

# Get the Report model from RPT schema
try:
    Report = AutomapBase.classes.get("RPT.Report")
except Exception as e:
    raise Exception(f"Failed to map Report table: {str(e)}")

# Export the model
__all__ = ["Report"]
