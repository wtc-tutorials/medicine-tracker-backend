# app/schemas.py
from datetime import datetime, date, time
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from enum import Enum


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"


# --- Dosage ---
class DosageBase(BaseModel):
    time_of_day: time
    quantity: int


class DosageCreate(DosageBase):
    pass


class Dosage(DosageBase):
    id: UUID
    medicine_id: UUID

    model_config = ConfigDict(from_attributes=True)


# --- Medicine ---
class MedicineBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    total_quantity: int


class MedicineCreate(MedicineBase):
    dosages: List[DosageCreate]


class Medicine(MedicineBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    dosages: List[Dosage]

    model_config = ConfigDict(from_attributes=True)


# --- User ---
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    date_of_birth: Optional[date] = None
    gender: Optional[GenderEnum] = None


class User(UserBase):
    id: UUID
    created_at: datetime
    date_of_birth: Optional[date] = None
    gender: Optional[GenderEnum] = None
    medicines: List[Medicine] = []

    model_config = ConfigDict(from_attributes=True)
