# backend/app/schemas.py
import uuid
from datetime import date, time, datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# Base that enables "from_attributes" (== old orm_mode)
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# --- Users ---
class UserBase(BaseSchema):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime


# --- Medicines ---
class MedicineBase(BaseSchema):
    name: str
    start_date: date
    total_quantity: int
    daily_dosage: int


class MedicineCreate(MedicineBase):
    pass


class MedicineResponse(MedicineBase):
    id: uuid.UUID
    owner_id: uuid.UUID


# --- Dosages ---
class DosageBase(BaseSchema):
    time_of_day: time
    quantity: int


class DosageCreate(DosageBase):
    pass


class DosageResponse(DosageBase):
    id: uuid.UUID
    medicine_id: uuid.UUID
