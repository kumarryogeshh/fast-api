"""
Pydantic schemas module.
Contains base Pydantic models for request/response validation.
"""

from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

# Generic type for ID field
T = TypeVar("T")


class BaseSchema(BaseModel):
    """
    Base schema with common configuration.
    """

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ResponseSchema(BaseSchema, Generic[T]):
    """
    Generic response schema for consistent API responses.
    """

    success: bool
    message: str
    data: Optional[T] = None
