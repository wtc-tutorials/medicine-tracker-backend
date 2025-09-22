# schemas.py
from pydantic import BaseModel
from datetime import date
from typing import Optional


class MedicineBase(BaseModel):
    name: str
    start_date: date
    total_quantity: int
    daily_dosage: int


class MedicineCreate(MedicineBase):
    pass


class Medicine(MedicineBase):
    id: int
    end_date: date
    remaining: int

    class Config:
        orm_mode = True
