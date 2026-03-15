# Base class for defining Pydantic models
from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    """
    Request body schema for creating a new employee.
    """

    # Employee name
    name: str

    # Department ID to which the employee belongs
    department_id: int


class EmployeeResponse(BaseModel):
    """
    Response schema for returning employee details.
    """

    # Employee ID from database
    id: int

    # Employee name
    name: str

    # Related department ID
    department_id: int

    class Config:
        # Allows Pydantic to read data from SQLAlchemy ORM objects
        orm_mode = True