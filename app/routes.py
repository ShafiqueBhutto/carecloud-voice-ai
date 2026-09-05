from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .database import get_db
from . import crud
from .schemas import PatientCreate, PatientUpdate, PatientResponse


router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("/")
def list_patients(
    last_name: Optional[str] = Query(None),
    date_of_birth: Optional[date] = Query(None),
    phone_number: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    patients = crud.get_patients(
        db=db,
        last_name=last_name,
        date_of_birth=date_of_birth,
        phone_number=phone_number
    )

    return {
        "data": patients,
        "error": None
    }


@router.get("/{patient_id}")
def get_patient(
    patient_id: str,
    db: Session = Depends(get_db)
):
    patient = crud.get_patient(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    return {
        "data": patient,
        "error": None
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):
    existing_patient = crud.get_patient_by_phone(
        db,
        patient.phone_number
    )

    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A patient with this phone number already exists"
        )

    new_patient = crud.create_patient(db, patient)

    return {
        "data": new_patient,
        "error": None
    }


@router.put("/{patient_id}")
def update_patient(
    patient_id: str,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db)
):
    patient = crud.get_patient(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    if patient_update.phone_number:
        existing_patient = crud.get_patient_by_phone(
            db,
            patient_update.phone_number
        )

        if (
            existing_patient
            and existing_patient.patient_id != patient_id
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A patient with this phone number already exists"
            )

    updated_patient = crud.update_patient(
        db,
        patient,
        patient_update
    )

    return {
        "data": updated_patient,
        "error": None
    }


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: str,
    db: Session = Depends(get_db)
):
    patient = crud.get_patient(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    deleted_patient = crud.delete_patient(db, patient)

    return {
        "data": deleted_patient,
        "error": None
    }