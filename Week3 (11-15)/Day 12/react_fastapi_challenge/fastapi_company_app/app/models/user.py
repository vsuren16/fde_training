# SQLAlchemy column data types
from sqlalchemy import Column, Integer, String

# Base class for all ORM models
from app.database import Base


class User(Base):
    """
    User model represents application users.
    This table is mainly used for authentication and authorization.
    """

    # Database table name
    __tablename__ = "users"

    # Primary key
    # Uniquely identifies each user record
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Username used for login
    # - unique=True → usernames must be unique
    # - index=True → improves login query performance
    # - nullable=False → username is mandatory
    username = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    # Stores the hashed password (never plain text)
    hashed_password = Column(
        String,
        nullable=False
    )

    # Role of the user (example: "admin", "user")
    # Used for role-based access control (RBAC)
    role = Column(
        String,
        nullable=False
    )