# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from . import models, schemas


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalars().first()


async def get_user(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(models.User)
        .options(selectinload(models.User.medicines))
        .where(models.User.id == user_id)
    )
    return result.scalars().first()


async def create_medicine(
    db: AsyncSession, medicine: schemas.MedicineCreate, user_id: str
):
    db_medicine = models.Medicine(
        **medicine.model_dump(exclude={"dosages"}), user_id=user_id
    )
    db.add(db_medicine)
    await db.flush()

    for dosage in medicine.dosages:
        db_dosage = models.Dosage(**dosage.model_dump(), medicine_id=db_medicine.id)
        db.add(db_dosage)

    await db.commit()
    await db.refresh(db_medicine)
    return db_medicine


async def get_medicines(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(models.Medicine)
        .options(selectinload(models.Medicine.dosages))
        .where(models.Medicine.user_id == user_id)
    )
    return result.scalars().all()
