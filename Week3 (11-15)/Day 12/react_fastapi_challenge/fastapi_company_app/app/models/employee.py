# SQLAlchemy column types and ForeignKey for table relationships
from sqlalchemy import Column, Integer, String, ForeignKey

# Used to define ORM relationships
from sqlalchemy.orm import relationship

# Base class for all database models
from app.database import Base


class Employee(Base):
    """
    Employee model represents an employee table in the database.
    Each employee belongs to exactly one department.
    """

    # Name of the table in the database
    __tablename__ = "employees"

    # Primary key column (unique identifier for each employee)
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Employee name
    # nullable=False → name is mandatory
    name = Column(
        String,
        nullable=False
    )

    # Foreign key column
    # This creates a link to departments.id
    department_id = Column(
        Integer,
        ForeignKey("departments.id")
    )

    # Relationship with Department table
    # - "Department" → related model
    # - back_populates → connects to employees field in Department model
    department = relationship(
        "Department",
        back_populates="employees"
    )