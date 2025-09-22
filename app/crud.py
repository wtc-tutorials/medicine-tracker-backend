# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from . import models, schemas


async def create_medicine(
    db: AsyncSession, medicine: schemas.MedicineCreate, user_id: int
):
    new_med = models.Medicine(
        name=medicine.name,
        start_date=medicine.start_date,
        total_quantity=medicine.total_quantity,
        daily_dosage=medicine.daily_dosage,
        owner_id=user_id,
    )
    db.add(new_med)
    await db.commit()
    await db.refresh(new_med)
    return new_med


async def get_medicines(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.Medicine).where(models.Medicine.owner_id == user_id)
    )
    return result.scalars().all()
