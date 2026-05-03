from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.seat import Seat
from app.models.booking import Booking
import time
from app.core.logger import get_logger
import datetime

from app.services.task import send_booking_email
from app.core.deps import get_current_user

router = APIRouter()
logger = get_logger(__name__)

@router.post("/book/{seat_id}")
def book_seat(seat_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        logger.info(f"Incoming booking request seat_id={seat_id}")
        logger.info(f"START seat_id={seat_id} time={datetime.datetime.now()}")
        # implementing lock on update to prevent race condition 
        seat = db.query(Seat).filter(Seat.id == seat_id).with_for_update().first()

        if not seat:
            logger.warning(f"Seat not found seat_id={seat_id}")
            raise HTTPException(status_code=404, detail="Seat not found")
        
        logger.info(f"Seat found status={seat.status}")

        if seat.status.lower() != "available":
            logger.warning(f"Seat already booked seat_id={seat_id}")
            return {"status": "failed", "message": "Already booked"}
        
        # Mark seat as booked BEFORE committing
        seat.status = "booked"

        booking = Booking(user_id=current_user.id, seat_id=seat_id, status="confirmed")

        db.add(booking)
        logger.info("Before commit (still holding lock)")
        db.commit()
        db.refresh(booking)

        logger.info(f"Booking successful booking_id={booking.id}")

        logger.info("Triggering Celery task: send_booking_email")
        # Trigger async task to send email notification
        task = send_booking_email.delay(user_id=booking.user_id, seat_id=booking.seat_id)

        logger.info(f"Task sent to queue task_id={task.id}")

        return {
            "status": "success",
            "message": "बुकिंग हो गई 😄"
        }

    except IntegrityError:
        db.rollback()
        logger.error(f"Integrity error seat_id={seat_id}")

        return {
            "status": "failed",
            "message": "Seat already booked"
        }