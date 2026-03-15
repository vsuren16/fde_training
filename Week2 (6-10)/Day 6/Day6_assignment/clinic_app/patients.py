from fastapi import APIRouter, Body, HTTPException, Path, Query

router = APIRouter(prefix="/patients", tags=["patients"])

patients_db: dict[int, dict] = {}

@router.post("/{patient_id}")
def create_patient(
    patient_id: int = Path(..., gt=0, description="Patient ID must be > 0"),
    gender: str = Query(..., description="Gender must be one of: male, female, other"),
    name: str = Body(..., min_length=3, embed=True),
    age: int = Body(..., ge=0, embed=True),
    contact_number: str = Body(..., embed=True),
):
    # Validate gender via query parameter
    allowed_genders = {"male", "female", "other"}
    if gender not in allowed_genders:
        raise HTTPException(
            status_code=422,
            detail="Invalid gender. Allowed values: male, female, other.",
        )

    # Duplicate patient_id not allowed
    if patient_id in patients_db:
        raise HTTPException(
            status_code=409,
            detail=f"Patient with patient_id={patient_id} already exists.",
        )

    # Contact number must be exactly 10 digits
    if not (contact_number.isdigit() and len(contact_number) == 10):
        raise HTTPException(
            status_code=422,
            detail="Invalid contact_number. It must be exactly 10 digits.",
        )

    patients_db[patient_id] = {
        "patient_id": patient_id,
        "name": name,
        "age": age,
        "contact_number": contact_number,
        "gender": gender,
    }

    return {
        "message": "Patient created successfully.",
        "patient": patients_db[patient_id],
    }


@router.get("/{patient_id}")
def read_patient(
    patient_id: int = Path(..., gt=0, description="Patient ID must be > 0")
):
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with patient_id={patient_id} not found.",
        )

    return {"patient": patients_db[patient_id]}


@router.put("/{patient_id}")
def update_patient(
    patient_id: int = Path(..., gt=0, description="Patient ID must be > 0"),
    gender: str = Query(..., description="Gender must be one of: male, female, other"),
    name: str = Body(..., min_length=3, embed=True),
    age: int = Body(..., ge=0, embed=True),
    contact_number: str = Body(..., embed=True),
):
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with patient_id={patient_id} not found.",
        )

    # Validate gender via query parameter
    allowed_genders = {"male", "female", "other"}
    if gender not in allowed_genders:
        raise HTTPException(
            status_code=422,
            detail="Invalid gender. Allowed values: male, female, other.",
        )

    # Contact number must be exactly 10 digits
    if not (contact_number.isdigit() and len(contact_number) == 10):
        raise HTTPException(
            status_code=422,
            detail="Invalid contact_number. It must be exactly 10 digits.",
        )

    patients_db[patient_id].update(
        {
            "name": name,
            "age": age,
            "contact_number": contact_number,
            "gender": gender,
        }
    )

    return {
        "message": "Patient updated successfully.",
        "patient": patients_db[patient_id],
    }


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int = Path(..., gt=0, description="Patient ID must be > 0")
):
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with patient_id={patient_id} not found.",
        )

    deleted = patients_db.pop(patient_id)
    return {"message": "Patient deleted successfully.", "patient": deleted}
