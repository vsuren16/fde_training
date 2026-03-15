from fastapi import FastAPI
from patients import router as patients_router
from appointments import router as appointments_router

app = FastAPI(title="Clinic Management System")

# Include routers
app.include_router(patients_router)
app.include_router(appointments_router)

# Run using:
# uvicorn main:app --reload