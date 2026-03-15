# FastAPI utilities for routing, dependencies, and error handling
from fastapi import APIRouter, Depends, HTTPException, status

# SQLAlchemy session for database operations
from sqlalchemy.orm import Session

# Database session dependency
from app.database import get_db

# Department ORM model
from app.models import Department

# Security dependencies
# - get_current_user → validates JWT
# - admin_only → allows only admin users
from app.core.security import get_current_user, admin_only


# Department router
# - All routes require a valid JWT (dependencies)
# - Grouped under "Departments" in Swagger UI
router = APIRouter(
    tags=["Departments"],
    dependencies=[Depends(get_current_user)]  # JWT required for all routes
)


# ============================
# CREATE DEPARTMENT (ADMIN)
# ============================
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_department(
    name: str,
    db: Session = Depends(get_db),
    user: dict = Depends(admin_only)
):
    """
    Creates a new department.
    Only admin users are allowed to access this API.
    """

    # Check if department with same name already exists
    existing = (
        db.query(Department)
        .filter(Department.name == name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department already exists"
        )

    # Create and save new department
    department = Department(name=name)
    db.add(department)
    db.commit()
    db.refresh(department)

    return {
        "message": "Department created successfully",
        "department": department
    }


# ============================
# LIST DEPARTMENTS (ANY USER)
# ============================
@router.get("/")
def get_departments(
    db: Session = Depends(get_db)
):
    """
    Returns all departments.
    Any authenticated user can access this API.
    """

    return db.query(Department).all()