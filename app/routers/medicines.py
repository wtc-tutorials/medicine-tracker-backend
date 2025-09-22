# medicines.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from .. import schemas, crud, database

router = APIRouter()


async def get_db():
    async with database.SessionLocal() as session:
        yield session


@router.post("/", response_model=schemas.Medicine)
async def create_medicine(
    medicine: schemas.MedicineCreate, db: AsyncSession = Depends(get_db)
):
    user_id = 1  # TODO: replace with auth
    med = await crud.create_medicine(db, medicine, user_id)
    end_date = medicine.start_date + timedelta(
        days=medicine.total_quantity // medicine.daily_dosage
    )
    remaining = medicine.total_quantity
    return schemas.Medicine(
        id=med.id,
        name=med.name,
        start_date=med.start_date,
        total_quantity=med.total_quantity,
        daily_dosage=med.daily_dosage,
        end_date=end_date,
        remaining=remaining,
    )


@router.get("/", response_model=list[schemas.Medicine])
async def list_medicines(db: AsyncSession = Depends(get_db)):
    user_id = 1  # TODO: replace with auth
    meds = await crud.get_medicines(db, user_id)
    output = []
    for m in meds:
        end_date = m.start_date + timedelta(days=m.total_quantity // m.daily_dosage)
        remaining = m.total_quantity  # TODO: update as usage tracked
        output.append(
            schemas.Medicine(
                id=m.id,
                name=m.name,
                start_date=m.start_date,
                total_quantity=m.total_quantity,
                daily_dosage=m.daily_dosage,
                end_date=end_date,
                remaining=remaining,
            )
        )
    return output
