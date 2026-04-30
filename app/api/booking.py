from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.seat import Seat
from app.models.booking import Booking
import time

router = APIRouter()


@router.post("/book/{seat_id}")
def book_seat(seat_id: int, db: Session = Depends(get_db)):
    try:
        seat = db.query(Seat).filter(Seat.id == seat_id).first()

        print(f"Booking request for seat_id: {seat_id}, found seat: {seat.id if seat else 'None'}")

        if not seat:
            raise HTTPException(status_code=404, detail="Seat not found")

        # simulate delay (your race condition test)
        time.sleep(5)

        booking = Booking(
            user_id=1,
            seat_id=seat_id,
            status="pending"
        )

        db.add(booking)

        # try commit (this is where DB enforces uniqueness)
        db.commit()
        db.refresh(booking)

        return {
            "status": "success",
            "message": "बुकिंग हो गई 😄"
        }

    except IntegrityError:
        db.rollback()

        return {
            "status": "failed",
            "message": "Seat already booked"
        }