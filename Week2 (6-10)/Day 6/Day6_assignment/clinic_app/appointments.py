from fastapi import APIRouter, Body, HTTPException, Path, Query

router = APIRouter(prefix="/appointments", tags=["appointments"])


appointments_db: dict[int, dict] = {}


@router.post("/{appointment_id}")
def create_appointment(
    appointment_id: int = Path(..., gt=0, description="Appointment ID must be > 0"),
    specialization: str = Query(
        ..., description="Specialization must be one of: general, cardiology, orthopedics"
    ),
    doctor_name: str = Body(..., min_length=3, embed=True),
    available_slots: int = Body(..., ge=1, embed=True),
):
    # Validate specialization via query parameter
    allowed_specs = {"general", "cardiology", "orthopedics"}
    if specialization not in allowed_specs:
        raise HTTPException(
            status_code=422,
            detail="Invalid specialization. Allowed values: general, cardiology, orthopedics.",
        )

    # Duplicate appointment_id not allowed
    if appointment_id in appointments_db:
        raise HTTPException(
            status_code=409,
            detail=f"Appointment with appointment_id={appointment_id} already exists.",
        )

    appointments_db[appointment_id] = {
        "appointment_id": appointment_id,
        "doctor_name": doctor_name,
        "available_slots": available_slots,
        "specialization": specialization,
    }

    return {
        "message": "Appointment created successfully.",
        "appointment": appointments_db[appointment_id],
    }


@router.get("/{appointment_id}")
def read_appointment(
    appointment_id: int = Path(..., gt=0, description="Appointment ID must be > 0")
):
    if appointment_id not in appointments_db:
        raise HTTPException(
            status_code=404,
            detail=f"Appointment with appointment_id={appointment_id} not found.",
        )

    return {"appointment": appointments_db[appointment_id]}


@router.put("/{appointment_id}")
def update_slots(
    appointment_id: int = Path(..., gt=0, description="Appointment ID must be > 0"),
    available_slots: int = Body(..., embed=True),
):
    """
    Update only the available slots.
    Validation rule: available slots must not go below zero.
    """
    if appointment_id not in appointments_db:
        raise HTTPException(
            status_code=404,
            detail=f"Appointment with appointment_id={appointment_id} not found.",
        )

    # Must not go below zero
    if available_slots < 0:
        raise HTTPException(
            status_code=422,
            detail="Invalid available_slots. It must not be below zero.",
        )

    appointments_db[appointment_id]["available_slots"] = available_slots

    return {
        "message": "Available slots updated successfully.",
        "appointment": appointments_db[appointment_id],
    }


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int = Path(..., gt=0, description="Appointment ID must be > 0")
):
    if appointment_id not in appointments_db:
        raise HTTPException(
            status_code=404,
            detail=f"Appointment with appointment_id={appointment_id} not found.",
        )

    deleted = appointments_db.pop(appointment_id)
    return {"message": "Appointment deleted successfully.", "appointment": deleted}
