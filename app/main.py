# main.py
from fastapi import FastAPI
from .routers import medicines
from .database import Base, engine
from . import models


# ✅ Create tables in the connected DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Medicine Tracker API")


app.include_router(medicines.router, prefix="/medicines", tags=["medicines"])


@app.get("/")
def root():
    return {"message": "Medicine Tracker API running"}
