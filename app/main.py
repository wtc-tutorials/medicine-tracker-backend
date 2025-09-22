# backend/app/main.py
from fastapi import FastAPI
from .routers import medicines
from .database import engine, Base

app = FastAPI(title="Medicine Tracker API")


# ✅ async table creation
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# run init once at startup
@app.on_event("startup")
async def on_startup():
    await init_models()


app.include_router(medicines.router, prefix="/medicines", tags=["medicines"])


@app.get("/")
def root():
    return {"message": "Medicine Tracker API running"}
