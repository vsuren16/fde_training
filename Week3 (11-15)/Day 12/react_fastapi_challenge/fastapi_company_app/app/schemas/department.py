# Base class for creating Pydantic models
from pydantic import BaseModel

# Used for handling lists of response objects (future use)
from typing import List


class DepartmentCreate(BaseModel):
    """
    Request body schema for creating a new department.
    """

    # Name of the department
    name: str


class DepartmentResponse(BaseModel):
    """
    Response schema for returning department data.
    """

    # Department ID (from database)
    id: int

    # Department name
    name: str

    class Config:
        # Enables compatibility with SQLAlchemy ORM objects
        # Allows returning ORM models directly from API
        orm_mode = True