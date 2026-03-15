# FastAPI utilities for routing, dependencies, and HTTP errors
from fastapi import APIRouter, Depends, HTTPException, status

# SQLAlchemy session for database access
from sqlalchemy.orm import Session

# Database session dependency
from app.database import get_db

# ORM models
from app.models import Employee, Department

# Security dependencies
# - get_current_user → validates JWT
# - admin_only → allows only admin users
from app.core.security import get_current_user, admin_only


# Employee router
# - All routes require authentication (JWT)
# - Grouped under "Employees" in Swagger UI
router = APIRouter(
    tags=["Employees"],
    dependencies=[Depends(get_current_user)]  # JWT required for all routes
)


# ============================
# CREATE EMPLOYEE (ADMIN ONLY)
# ============================
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_employee(
    name: str,
    department_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(admin_only)
):
    """
    Creates a new employee.
    Only admin users are allowed to access this API.
    """

    # Check if the department exists
    department = (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    # Create and save new employee
    employee = Employee(
        name=name,
        department_id=department_id
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


# ============================
# LIST EMPLOYEES (ANY USER)
# ============================
@router.get("/", status_code=status.HTTP_200_OK)
def list_employees(
    db: Session = Depends(get_db)
):
    """
    Returns all employees.
    Any authenticated user can access this API.
    """

    return db.query(Employee).all()