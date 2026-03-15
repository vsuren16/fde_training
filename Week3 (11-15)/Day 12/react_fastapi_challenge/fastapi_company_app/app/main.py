# Core FastAPI application class
from fastapi import FastAPI

# Database engine and Base for table creation
from app.database import Base, engine

# Routers for different modules
from app.routes.auth_routes import router as auth_router
from app.routes.department_routes import router as department_router
from app.routes.employee_routes import router as employee_router

# Middleware to handle Cross-Origin Resource Sharing (CORS)
from fastapi.middleware.cors import CORSMiddleware


# Create database tables
# This creates all tables defined using SQLAlchemy models
# (users, departments, employees, etc.)
Base.metadata.create_all(bind=engine)

# Create FastAPI application instance
app = FastAPI()


# ============================
# CORS CONFIGURATION
# ============================
# Allows frontend (React/Vite) to communicate with FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React (Vite) frontend URL
    allow_credentials=True,
    allow_methods=["*"],   # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],   # Allow all headers (Authorization, Content-Type)
)


# ============================
# ROUTER REGISTRATION
# ============================
# Mount different API modules with URL prefixes

# Authentication routes
app.include_router(auth_router, prefix="/auth")

# Department-related routes
app.include_router(department_router, prefix="/departments")

# Employee-related routes
app.include_router(employee_router, prefix="/employees")