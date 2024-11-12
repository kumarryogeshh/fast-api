"""
Base models module.
Handles database reflection and model creation using SQLAlchemy automap.
"""

from sqlalchemy.ext.automap import automap_base
from app.core.database import engine

# Create automap base
Base = automap_base()

# Reflect the database schema
Base.prepare(engine, reflect=True)
