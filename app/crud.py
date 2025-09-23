import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas


# --- User CRUD ---
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password,  # 🚨 TODO: hash before storing!
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: uuid.UUID):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalar_one_or_none()


# --- Medicine CRUD ---
async def create_medicine(
    db: AsyncSession, medicine: schemas.MedicineCreate, owner_id: uuid.UUID
):
    db_medicine = models.Medicine(**medicine.dict(), owner_id=owner_id)
    db.add(db_medicine)
    await db.commit()
    await db.refresh(db_medicine)
    return db_medicine


async def get_medicines(db: AsyncSession, owner_id: uuid.UUID):
    result = await db.execute(
        select(models.Medicine).filter(models.Medicine.owner_id == owner_id)
    )
    return result.scalars().all()


# --- Dosage CRUD ---
async def create_dosage(
    db: AsyncSession, dosage: schemas.DosageCreate, medicine_id: uuid.UUID
):
    db_dosage = models.Dosage(**dosage.dict(), medicine_id=medicine_id)
    db.add(db_dosage)
    await db.commit()
    await db.refresh(db_dosage)
    return db_dosage


async def get_dosages(db: AsyncSession, medicine_id: uuid.UUID):
    result = await db.execute(
        select(models.Dosage).filter(models.Dosage.medicine_id == medicine_id)
    )
    return result.scalars().all()
