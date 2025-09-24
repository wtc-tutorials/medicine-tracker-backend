from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/medicines", tags=["medicines"])



@router.post("/", response_model=schemas.MedicineResponse)
async def create_medicine(
    medicine: schemas.MedicineCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Create a new medicine for the authenticated user."""
    db_medicine = models.Medicine(
        **medicine.model_dump(),  # use model_dump() instead of dict()
        owner_id=current_user.id,
    )
    db.add(db_medicine)
    await db.commit()
    await db.refresh(db_medicine)
    return db_medicine


@router.get("/", response_model=List[schemas.MedicineResponse])
async def list_medicines(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """List all medicines for the authenticated user."""
    result = await db.execute(
        models.Medicine.__table__.select().where(
            models.Medicine.owner_id == current_user.id
        )
    )
    medicines = result.scalars().all()
    return medicines


@router.get("/{medicine_id}", response_model=schemas.MedicineResponse)
async def get_medicine(
    medicine_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Get a specific medicine by ID for the authenticated user."""
    result = await db.execute(
        models.Medicine.__table__.select().where(
            (models.Medicine.id == medicine_id)
            & (models.Medicine.owner_id == current_user.id)
        )
    )
    medicine = result.scalar_one_or_none()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Medicine not found"
        )
    return medicine


@router.delete("/{medicine_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medicine(
    medicine_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Delete a specific medicine by ID for the authenticated user."""
    result = await db.execute(
        models.Medicine.__table__.select().where(
            (models.Medicine.id == medicine_id)
            & (models.Medicine.owner_id == current_user.id)
        )
    )
    medicine = result.scalar_one_or_none()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Medicine not found"
        )

    await db.delete(medicine)
    await db.commit()
