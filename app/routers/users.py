# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, database

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)
):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)
