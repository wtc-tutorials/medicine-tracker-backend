# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
database = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

# print(f"\n{DATABASE_URL = }")

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# class Base(DeclarativeBase):
#     pass
