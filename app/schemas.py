from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
import re


class PatientBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)

    date_of_birth: date

    sex: str

    phone_number: str

    email: Optional[EmailStr] = None

    address_line_1: str = Field(..., min_length=1)
    address_line_2: Optional[str] = None

    city: str = Field(..., min_length=1, max_length=100)

    state: str = Field(..., min_length=2, max_length=2)

    zip_code: str

    insurance_provider: Optional[str] = None
    insurance_member_id: Optional[str] = None

    preferred_language: Optional[str] = "English"

    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", value.strip()):
            raise ValueError(
                "Name must contain only letters, hyphens, or apostrophes"
            )
        return value.strip()

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return value

    @field_validator("sex")
    @classmethod
    def validate_sex(cls, value: str) -> str:
        allowed = {
            "Male",
            "Female",
            "Other",
            "Decline to Answer"
        }

        normalized = value.strip().title()

        if normalized not in allowed:
            raise ValueError(
                "Sex must be Male, Female, Other, or Decline to Answer"
            )

        return normalized

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        digits = re.sub(r"\D", "", value)

        if len(digits) == 11 and digits.startswith("1"):
            digits = digits[1:]

        if len(digits) != 10:
            raise ValueError(
                "Phone number must be a valid U.S. 10-digit number"
            )

        return digits

    @field_validator("state")
    @classmethod
    def validate_state(cls, value: str) -> str:
        value = value.strip().upper()

        if not re.fullmatch(r"[A-Z]{2}", value):
            raise ValueError(
                "State must be a valid 2-letter U.S. state abbreviation"
            )

        return value

    @field_validator("zip_code")
    @classmethod
    def validate_zip_code(cls, value: str) -> str:
        value = value.strip()

        if not re.fullmatch(r"\d{5}(?:-\d{4})?", value):
            raise ValueError(
                "ZIP code must be 5 digits or ZIP+4 format"
            )

        return value

    @field_validator("emergency_contact_phone")
    @classmethod
    def validate_emergency_phone(
        cls,
        value: Optional[str]
    ) -> Optional[str]:

        if value is None:
            return None

        digits = re.sub(r"\D", "", value)

        if len(digits) == 11 and digits.startswith("1"):
            digits = digits[1:]

        if len(digits) != 10:
            raise ValueError(
                "Emergency contact phone must be a valid U.S. 10-digit number"
            )

        return digits


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    first_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50
    )

    last_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50
    )

    date_of_birth: Optional[date] = None
    sex: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None

    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None

    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

    insurance_provider: Optional[str] = None
    insurance_member_id: Optional[str] = None

    preferred_language: Optional[str] = None

    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value):
        if value is not None and value > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return value

    @field_validator("phone_number", "emergency_contact_phone")
    @classmethod
    def validate_phone(cls, value):
        if value is None:
            return None

        digits = re.sub(r"\D", "", value)

        if len(digits) == 11 and digits.startswith("1"):
            digits = digits[1:]

        if len(digits) != 10:
            raise ValueError(
                "Phone number must be a valid U.S. 10-digit number"
            )

        return digits


class PatientResponse(PatientBase):
    patient_id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)