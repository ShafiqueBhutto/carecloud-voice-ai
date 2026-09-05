from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from . import models
from .schemas import PatientCreate, PatientUpdate


def get_patients(
    db: Session,
    last_name: Optional[str] = None,
    date_of_birth=None,
    phone_number: Optional[str] = None,
):
    query = db.query(models.Patient).filter(
        models.Patient.deleted_at.is_(None)
    )

    if last_name:
        query = query.filter(
            models.Patient.last_name.ilike(last_name)
        )

    if date_of_birth:
        query = query.filter(
            models.Patient.date_of_birth == date_of_birth
        )

    if phone_number:
        query = query.filter(
            models.Patient.phone_number == phone_number
        )

    return query.order_by(models.Patient.created_at.desc()).all()


def get_patient(
    db: Session,
    patient_id: str
):
    return (
        db.query(models.Patient)
        .filter(
            models.Patient.patient_id == patient_id,
            models.Patient.deleted_at.is_(None)
        )
        .first()
    )


def get_patient_by_phone(
    db: Session,
    phone_number: str
):
    return (
        db.query(models.Patient)
        .filter(
            models.Patient.phone_number == phone_number,
            models.Patient.deleted_at.is_(None)
        )
        .first()
    )


def create_patient(
    db: Session,
    patient: PatientCreate
):
    db_patient = models.Patient(
        **patient.model_dump()
    )

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    return db_patient


def update_patient(
    db: Session,
    db_patient: models.Patient,
    patient_update: PatientUpdate
):
    update_data = patient_update.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(db_patient, field, value)

    db_patient.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_patient)

    return db_patient


def delete_patient(
    db: Session,
    db_patient: models.Patient
):
    db_patient.deleted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_patient)

    return db_patient