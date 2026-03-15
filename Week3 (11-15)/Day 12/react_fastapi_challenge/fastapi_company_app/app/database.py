# Used to create database engine and ORM base
from sqlalchemy import create_engine

# Used to create database sessions
from sqlalchemy.orm import sessionmaker, declarative_base


# Database connection URL
# SQLite database stored as a local file (company.db)
DATABASE_URL = "sqlite:///./company.db"

# Create the SQLAlchemy engine
# check_same_thread=False is required for SQLite with FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a session factory
# - autocommit=False → changes must be committed manually
# - autoflush=False → prevents automatic DB writes
# - bind=engine → connects sessions to the database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class that all ORM models will inherit from
Base = declarative_base()


def get_db():
    """
    Provides a database session to API routes.

    This function is used with FastAPI's Depends()
    to ensure each request gets its own DB session
    and that the session is properly closed after use.
    """

    # Create a new database session
    db = SessionLocal()

    try:
        # Yield the session to the API route
        yield db
    finally:
        # Always close the session after request completes
        db.close()