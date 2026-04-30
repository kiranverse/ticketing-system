# app/main.py
from fastapi import FastAPI
from app.api.booking import router as booking_router
from app.models import *
from app.core.logger import setup_logger

setup_logger()

app = FastAPI()
app.include_router(booking_router)

@app.get("/")
async def root():
    return {"message": "Ticketing System Running"}

app.include_router(booking_router)