# app/main.py
from fastapi import FastAPI
from app.api.booking import router as booking_router
from app.models import *
from app.core.logger import setup_logger
from app.api.user import router as user_router

setup_logger()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Ticketing System Running"}

app.include_router(user_router)
app.include_router(booking_router)
