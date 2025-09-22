# main.py
from fastapi import FastAPI
from .routers import medicines

app = FastAPI(title="Medicine Tracker API")

app.include_router(medicines.router, prefix="/medicines", tags=["medicines"])
