# app/main.py
from fastapi import FastAPI
from app.api.booking import router as booking_router
from app.models import *

app = FastAPI()
app.include_router(booking_router)

@app.get("/")
async def root():
    return {"message": "Ticketing System Running"}

app.include_router(booking_router)