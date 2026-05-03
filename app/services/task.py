# app/services/task.py

from app.models.user import User
from app.services.celery import app
from app.services.email_Service import send_email
from app.core.logger import get_logger
from app.core.deps import get_db
from app.core.database import SessionLocal

logger = get_logger(__name__)


@app.task(bind=True, name="send_email", max_retries=3)
def send_booking_email(self, user_id, seat_id):
    db = SessionLocal()
    try:
        logger.info(f"[Task START] task_id={self.request.id}")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise Exception("User not found")

        user_email = user.email
        subject = "Booking Confirmation 🎟️"
        body = f"Hi {user.name}, your seat {seat_id} is booked!"

        send_email(user_email, subject, body)

        logger.info(f"[Task END] Email sent to {user_email}")

    except Exception as e:
        raise self.retry(exc=e, countdown=5)

    finally:
        db.close()