# SQLAlchemy column types
from sqlalchemy import Column, Integer, String

# Used to define relationships between tables
from sqlalchemy.orm import relationship

# Base class for all database models
from app.database import Base


class Department(Base):
    """
    Department model represents a department table in the database.
    One department can have many employees.
    """

    # Name of the table in the database
    __tablename__ = "departments"

    # Primary key column (unique identifier for each department)
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Department name
    # - unique=True → no two departments can have the same name
    # - nullable=False → name is mandatory
    name = Column(
        String,
        unique=True,
        nullable=False
    )

    # Relationship with Employee table
    # - "Employee" → related model (string used to avoid circular import)
    # - back_populates → connects with department field in Employee model
    # - cascade="all, delete" → deleting a department deletes its employees
    employees = relationship(
        "Employee",
        back_populates="department",
        cascade="all, delete"
    )